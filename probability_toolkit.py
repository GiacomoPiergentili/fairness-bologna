MAX_VAL = 5

def const_val(val,t0,t1,t):
    if t>t0 and t<=t1: return val
    return 0

def ramp_val(val, t0, t1, t):
    if t>t0 and t<=t1:
        return val * (t - t0) / (t1 - t0)
    return 0

def children_prob(t):
    val = (
        ramp_val(1, 6,7.5,t)+\
        const_val(1,7.5,8.5,t)+\
        (const_val(1,8.5,9,t)-ramp_val(1, 8.5,9.1,t))+\

        const_val(0.2,9,12,t)+\

        ramp_val(1, 12,12.5,t)+\
        const_val(1,12.5,14,t)+\
        (const_val(1,14,15,t)-ramp_val(1, 14,15,t))+\

        const_val(0.2,15,20,t)
    )
    return max(0,val) # smoothing

def guys_prob(t):
    val = (
        0.5+\
        ramp_val(0.8, 6,7.5,t)+\
        const_val(0.8,7.5,22,t)+\
        (const_val(0.8,22,24,t)-ramp_val(0.8, 22,24,t)) 
    )
    return max(0.1,val) # smoothing

def man_prob(t):
    val = (
        ramp_val(1, 6,7.5,t)+\
        const_val(1,7.5,8.5,t)+\
        (const_val(1,8.5,9,t)-ramp_val(1, 8.5,9.1,t))+\

        const_val(0.5,9,15.6,t)+\

        ramp_val(1, 15.5,16,t)+\
        const_val(1,16,19,t)+\
        (const_val(1,19,20,t)-ramp_val(1, 19,20.1,t))+\

        const_val(0.5,20,24,t)
    )
    return max(0.1,val) # smoothing

def woman_prob(t):
    val = (
        0.1+
        ramp_val(0.9, 6,7.5,t)+\
        const_val(0.9,7.5,8.5,t)+\
        (const_val(0.9,8.5,9,t)-ramp_val(0.9, 8.5,9.1,t))+\

        const_val(0.5,9,12,t)+\

        ramp_val(0.9, 12,12.5,t)+\
        const_val(0.9,12.5,14,t)+\
        (const_val(0.9,14,15,t)-ramp_val(0.9, 14,15,t))+\

        const_val(0.5,15,20,t)
    )
    return max(0.1,val) # smoothing

def plot_probs():
    import numpy as np
    import matplotlib
    matplotlib.use('Qt5Agg')
    import matplotlib.pyplot as plt

    ts = np.linspace(0,24,num=100)
    
    vals = {
        'children_prob':{'function':children_prob,
                         'data':[]},
        'guys_prob':{'function':guys_prob,
                         'data':[]},
        'man_prob':{'function':man_prob,
                         'data':[]},
        'woman_prob':{'function':woman_prob,
                         'data':[]}
    }

    for key in vals.keys():
        for t in ts:
            vals[key]['data'].append(vals[key]['function'](t))
    
    n_plots=len(vals.keys())
    fig, axes = plt.subplots(nrows=n_plots, figsize=(5, 4*n_plots), sharex=True)

    for _,key in enumerate(vals.keys()):
        ax = axes[_]
        ax.plot(ts, vals[key]['data'])
        ax.set_title(key)
        ax.grid(':')
        ax.set_ylim(-0.2, 1.2)
    
    plt.tight_layout()
    plt.show()

if __name__=='__main__':
    plot_probs()