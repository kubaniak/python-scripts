import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import torch
import torch.fft
import tqdm

"""
Create Your Own Navier-Stokes Spectral Method Simulation (With Python)
Philip Mocz (2023), @PMocz

Simulate the Navier-Stokes equations (incompressible viscous fluid) 
with a Spectral method

v_t + (v.nabla) v = nu * nabla^2 v + nabla P
div(v) = 0

"""

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def poisson_solve(rho, kSq_inv):
    """ solve the Poisson equation, given source field rho """
    V_hat = -(torch.fft.fftn(rho)) * kSq_inv
    V = torch.real(torch.fft.ifftn(V_hat))
    return V

def diffusion_solve(v, dt, nu, kSq):
    """ solve the diffusion equation over a timestep dt, given viscosity nu """
    v_hat = (torch.fft.fftn(v)) / (1.0 + dt * nu * kSq)
    v = torch.real(torch.fft.ifftn(v_hat))
    return v

def grad(v, kx, ky):
    """ return gradient of v """
    v_hat = torch.fft.fftn(v)
    dvx = torch.real(torch.fft.ifftn(1j * kx * v_hat))
    dvy = torch.real(torch.fft.ifftn(1j * ky * v_hat))
    return dvx, dvy

def div(vx, vy, kx, ky):
    """ return divergence of (vx,vy) """
    dvx_x = torch.real(torch.fft.ifftn(1j * kx * torch.fft.fftn(vx)))
    dvy_y = torch.real(torch.fft.ifftn(1j * ky * torch.fft.fftn(vy)))
    return dvx_x + dvy_y

def curl(vx, vy, kx, ky):
    """ return curl of (vx,vy) """
    dvx_y = torch.real(torch.fft.ifftn(1j * ky * torch.fft.fftn(vx)))
    dvy_x = torch.real(torch.fft.ifftn(1j * kx * torch.fft.fftn(vy)))
    return dvy_x - dvx_y

def apply_dealias(f, dealias):
    """ apply 2/3 rule dealias to field f """
    f_hat = dealias * torch.fft.fftn(f)
    return torch.real(torch.fft.ifftn(f_hat))

def main():
    """ Navier-Stokes Simulation """
    
    # Simulation parameters
    N = 200     # Spatial resolution
    t = 0       # current time of the simulation
    tEnd = 2    # time at which simulation ends
    dt = 0.001  # timestep
    tOut = 0.01 # draw frequency
    nu = 0.005  # viscosity
    plotRealTime = True # switch on for plotting as the simulation goes along
    
    # Domain [0,1] x [0,1]
    L = 1    
    xlin = np.linspace(0, L, num=N+1)  # Note: x=0 & x=1 are the same point!
    xlin = xlin[0:N]                   # chop off periodic point
    xx, yy = np.meshgrid(xlin, xlin)
    zero = np.zeros_like(xx)
    one = np.ones_like(xx)
    r = xx*xx + yy*yy
    vx = one - (xx*xx - yy*yy)
    vy = zero
    # Initial Condition (vortex)
    vx = torch.tensor(vx, device=device, dtype=torch.float32)
    vy = torch.tensor(vy, device=device, dtype=torch.float32)
    
    # Fourier Space Variables
    klin = 2.0 * np.pi / L * np.arange(-N/2, N/2)
    kmax = np.max(klin)
    kx, ky = np.meshgrid(klin, klin)
    kx = torch.tensor(np.fft.ifftshift(kx), device=device, dtype=torch.float32)
    ky = torch.tensor(np.fft.ifftshift(ky), device=device, dtype=torch.float32)
    kSq = kx**2 + ky**2
    kSq_inv = 1.0 / kSq
    kSq_inv[kSq == 0] = 1
    
    # Dealias with the 2/3 rule
    dealias = torch.tensor((np.abs(kx.cpu()) < (2./3.)*kmax) & (np.abs(ky.cpu()) < (2./3.)*kmax), device=device)
    
    # Number of timesteps
    Nt = int(np.ceil(tEnd / dt))
    
    # Prep figure
    fig, ax = plt.subplots(figsize=(4,4), dpi=80)
    frames = []
    
    
    # Main Loop
    for i in tqdm.tqdm(range(Nt)):

        # Advection: rhs = -(v.grad)v
        dvx_x, dvx_y = grad(vx, kx, ky)
        dvy_x, dvy_y = grad(vy, kx, ky)
        
        rhs_x = -(vx * dvx_x + vy * dvx_y)
        rhs_y = -(vx * dvy_x + vy * dvy_y)
        
        rhs_x = apply_dealias(rhs_x, dealias)
        rhs_y = apply_dealias(rhs_y, dealias)

        vx += dt * rhs_x
        vy += dt * rhs_y
        
        # Poisson solve for pressure
        div_rhs = div(rhs_x, rhs_y, kx, ky)
        P = poisson_solve(div_rhs, kSq_inv)
        dPx, dPy = grad(P, kx, ky)
        
        # Correction (to eliminate divergence component of velocity)
        vx += - dt * dPx
        vy += - dt * dPy
        
        # Diffusion solve (implicit)
        vx = diffusion_solve(vx, dt, nu, kSq)
        vy = diffusion_solve(vy, dt, nu, kSq)
        
        # Vorticity (for plotting)
        wz = curl(vx, vy, kx, ky)
        
        # Update time
        t += dt
        # print(t)
        
        # Collect frames for animation
        if t + dt > (len(frames) + 1) * tOut or i == Nt-1:
            im = ax.imshow(wz.cpu().numpy(), cmap='RdBu', animated=True)
            ax.invert_yaxis()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            ax.set_aspect('equal')
            frames.append([im])
            
    # Create animation
    ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True)
    
    # Save animation
    ani.save('navier-stokes-spectral-animation.mp4', writer='ffmpeg', dpi=240)
    plt.show()

    return 0

if __name__ == "__main__":
    main()
