import matplotlib.pyplot as plt
from vqcd_main_funcs import *
from vqcd_secondary_funcs import *
from matplotlib import rcParams
import matplotlib.font_manager as font_manager

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 9

})


def average_fidelity(qdim, rank, an, noise_mdl, total_chan_no):

    tfb_big_list = []
    tgfb_big_list = []
    for any_chan_no in range(1,total_chan_no+1):
        
        error_list = np.load(f'data/fid_plot_data_test/qdim{qdim}_rank{rank}_error_list_{noise_mdl}_anychan{any_chan_no}.npy')
        
        tfb_small_list = []
        tgfb_small_list = []
        
        for error in error_list:

            x1 = np.load(f'data/fid_plot_data_test/qbit{qdim}_lower_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}.npy')
            x2 = np.load(f'data/fid_plot_data_test/qbit{qdim}_upper_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}.npy')
            tfb_small_list.append(float(x1))
            tgfb_small_list.append(float(x2))
        
        tfb_big_list.append(tfb_small_list)
        tgfb_big_list.append(tgfb_small_list)

    TFB_list = [0,0,0,0]
    TGFB_list = [0,0,0,0]

    for k in tfb_big_list:
        if len(k) == rank:
            TFB_list = np.add(k, TFB_list)
    
    for k in tgfb_big_list:
        if len(k) == rank:
            TGFB_list = np.add(k, TGFB_list)

    # LESS THAN 5%:
    TFB_list_less_than_5 = [0,0,0,0]
    TGFB_list_less_than_5 = [0,0,0,0]

    y = 0
    for l_no,l in enumerate(tfb_big_list):
        if len(l) == 4 and l[3] < 0.05:
            TFB_list_less_than_5 = np.add(TFB_list_less_than_5, l)
            y += 1

    print(y)
    for l_no,l in enumerate(tgfb_big_list):
        if len(l) == 4 and l[3] < 0.05:
            TGFB_list_less_than_5 = np.add(TGFB_list_less_than_5, l)

    print(TFB_list, TGFB_list, TFB_list_less_than_5, TGFB_list_less_than_5)


    m_list = list(range(1, rank+1))
    TFB_list = [x / total_chan_no for x in TFB_list]
    TGFB_list = [x / total_chan_no for x in TGFB_list]
    TFB_list_less_than_5 = [x / total_chan_no for x in TFB_list_less_than_5]
    TGFB_list_less_than_5 = [x / total_chan_no for x in TGFB_list_less_than_5]

    #y-error:
    TFB_std_big_list = []
    TGFB_std_big_list = []
    TFB_std_less_than_five_big_list = []
    TGFB_std_less_than_five_big_list = []
    
    for el in m_list:
        TFB_std_list = []
        TGFB_std_list = []
        TFB_std_less_than_five_list = []
        TGFB_std_less_than_five_list = []
        
        for tfb_list in tfb_big_list:
            if len(tfb_list) == 4:
                TFB_std_list.append(tfb_list[el-1])
            if len(tfb_list) == 4 and tfb_list[3] < 0.05:
                TFB_std_less_than_five_list.append(tfb_list[el-1])

        for tgfb_list in tgfb_big_list:
            if len(tgfb_list) == 4:
                TGFB_std_list.append(tgfb_list[el-1])
            if len(tgfb_list) == 4 and tgfb_list[3] < 0.05:
                TGFB_std_less_than_five_list.append(tgfb_list[el-1])
        
        TFB_std_big_list.append(TFB_std_list)
        TFB_std_less_than_five_big_list.append(TFB_std_less_than_five_list)
        TGFB_std_big_list.append(TGFB_std_list)
        TGFB_std_less_than_five_big_list.append(TGFB_std_less_than_five_list)

    TFB_std = []
    TGFB_std = []
    TFB_std_less_than_five = []
    TGFB_std_less_than_five = []
    for el in range(4):
        TFB_std.append(np.std(TFB_std_big_list[el]))
        TGFB_std.append(np.std(TGFB_std_big_list[el]))
        TFB_std_less_than_five.append(np.std(TFB_std_less_than_five_big_list[el]))
        TGFB_std_less_than_five.append(np.std(TGFB_std_less_than_five_big_list[el]))

    print(TFB_std)
    print(TGFB_std)
    print(TFB_std_less_than_five)
    print(TGFB_std_less_than_five)
   
    plt.figure(figsize=(3.5,2.625))
    plt.errorbar(m_list, TGFB_list, fmt = 'r-s', ecolor = 'red', yerr= TGFB_std, capsize = 3, label = '$\\Delta F_{\\star} (\\rho_{m},\\sigma_{m}^{\\rho})$', markeredgecolor='red', markerfacecolor='none', markersize=6)
    plt.errorbar(m_list, TFB_list, yerr= TFB_std, fmt = 'b-s', ecolor = 'blue', capsize = 3, label = '$\\Delta F (\\rho_{m},\\sigma_{m}^{\\rho})$', markeredgecolor='blue', markerfacecolor='none', markersize=6)
    plt.errorbar(m_list, TGFB_list_less_than_5, fmt = 'r--o', ecolor = 'red', capsize = 0.1, label = '$\\Delta F_{\\star} (\\rho_{m},\\sigma_{m}^{\\rho})$ ($<  5\\% $)', markeredgewidth = 1, markeredgecolor='red', markerfacecolor='none', markersize=6)
    plt.errorbar(m_list, TFB_list_less_than_5,  fmt = 'b--o', ecolor = 'blue', capsize = 0.1, label = '$\\Delta F (\\rho_{m},\\sigma_{m}^{\\rho})$ ($<  5\\% $)', markeredgecolor='blue', markerfacecolor='none', markersize=6)

    plt.xticks(m_list)
    plt.yticks()
    plt.xlabel('$m$')
    plt.ylabel('$\\Delta F (\\rho,\\sigma^{\\rho})$')
    plt.legend()
    #plt.show()

    plt.tight_layout()
    out_file = f'plot/qbit{qdim}_rank{rank}_truncated_fidelity_bound_chan{any_chan_no}.pdf'
    print("[INFO] Saving in", out_file)
    plt.savefig(f'plot/qbit{qdim}_rank{rank}_truncated_fidelity_bound_chan{any_chan_no}.pdf')


def single_chan_fidelity(qdim, rank, an, layers, device_type, noise_amp_list):
    """
    returns plot for a single channel
    """

    # TODO: why this is 730 and 765 ???
    if qdim == 1:
        any_chan_no = 730 #np.load(f'data/fid_plot_test/lowest_error_chan_qdim{qdim}_rank{rank}/.npy')
    elif qdim == 2:
        any_chan_no = 765

    noise_mdl_list = ['amp_damp', 'depol', 'rand_x']
    if device_type == 'sim':
        fig, ax = plt.subplots(nrows=1, ncols = len(noise_mdl_list),
                sharex=True, sharey=True, figsize=(7, 3))
    
    type_list =  ['-o', '--s', '-x', '--v', '-v']
    if device_type == 'sim':
        noise_mdl_list = ['amp_damp', 'depol', 'rand_x']
        noise_mdl_label = ['amp. dampling', 'depolarizing', 'random X']
    elif device_type == 'real':
        if qdim == 1:
            noise_mdl_list = ['ibmq_manila', 'ibmq_lima']
            noise_mdl_label = ['ibmq-manila', 'ibmq-lima']
        elif qdim == 2:
            noise_mdl_list = ['ibmq-manila', 'ibmq-lima']
            noise_mdl_label = ['ibmq-manila', 'ibmq-lima']
        noise_amp_list = [0]

    for noise_mdl_no, noise_mdl in enumerate(noise_mdl_list):
        for noise_amp_no, noise_amp in enumerate(noise_amp_list):
            
            error_list = np.load(f'data/fid_plot_data_test/qdim{qdim}_rank{rank}_error_list_{noise_mdl}_{noise_amp}.npy')
            mlist = np.load(f'data/fid_plot_data_test/qbit{qdim}_m_list_rank{rank}_ansatz{an}_{noise_mdl}_{noise_amp}.npy')
            true_fidelity = np.load(f'data/fid_plot_data_test/qbit{qdim}_true_fid_rank{rank}_ansatz{an}.npy')
            tfb_list = []
            tgfb_list = []
            tf_list = []
            layers_list_plot = []

            if device_type == 'real':
                layers_list = list(range(1, layers+1))
        
            elif device_type == 'sim':
                layers_list = list(range(layers, layers+1))
            
            for l in layers_list:

                for error in error_list:
                    tfb = np.load(f'data/fid_plot_data_test/qbit{qdim}_lower_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}_{device_type}{noise_mdl}_{noise_amp}_layers{l}.npy')
                    tgfb = np.load(f'data/fid_plot_data_test/qbit{qdim}_upper_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}_{device_type}{noise_mdl}_{noise_amp}_layers{l}.npy')
                    tfb_list.append(tfb)
                    tgfb_list.append(tgfb)
                    tf_list.append(true_fidelity)

                if len(layers_list) == 1:
                    
                    print(f'ranks {mlist} with error list {error_list} for noise model {noise_mdl} with amplitude {noise_amp}' )
                    if noise_mdl_no == 0:
                        ax[noise_mdl_no].plot(mlist, tfb_list, 'b'+type_list[noise_amp_no], label = '$F (\\rho_{m},\\sigma_{m}^{\\rho})$', markerfacecolor='none')
                        ax[noise_mdl_no].plot(mlist, tgfb_list, 'r'+type_list[noise_amp_no], label = '$F_{\\star} (\\rho_{m},\\sigma_{m}^{\\rho})$', markerfacecolor='none')
                        ax[1].set_xlabel('$m$')
                        ax[noise_mdl_no].set_ylabel('$F (\\rho,\\sigma^{\\rho})$')
                    else:
                        ax[noise_mdl_no].plot(mlist, tfb_list, 'b'+type_list[noise_amp_no], markerfacecolor='none')
                        ax[noise_mdl_no].plot(mlist, tgfb_list, 'r'+type_list[noise_amp_no], markerfacecolor='none')
                    
                    ax[noise_mdl_no].plot(mlist, tf_list, 'k-')
                    ax[noise_mdl_no].title.set_text(f'{noise_mdl_label[noise_mdl_no]} noise')
                    plt.xticks([1,2,3,4])
                
                layers_list_plot.append(l)

        if len(layers_list) > 1:
            tfb_noise_free_list = []
            
            for l in range(1, layers+1):
                tfb_noise_free = np.load(f'data/fid_plot_data_test/qbit{qdim}_lower_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}_simsimulator_0_layers{l}.npy')
                tfb_noise_free_list.append(tfb_noise_free)
        
            if l == 1 and l == 2 :
                plt.plot(layers_list_plot, tfb_list, '-o' )
                
            else:
                plt.plot(layers_list_plot, tfb_list, type_list[noise_mdl_no], label = f'{noise_mdl_label[noise_mdl_no]} simulator', markerfacecolor='none')

            plt.xticks(list(range(1, layers+1)))
            plt.yticks()
            plt.xlabel('Layers of ansatz')
            plt.ylabel('$F(\\rho,\\sigma^{\\rho})$')
    if device_type == 'sim':
        # fig.legend( bbox_to_anchor=(1., 0.5), ncol=1, borderaxespad=0.8)
        plt.subplots_adjust(bottom=0.14)
    else:
        plt.plot(layers_list_plot, tfb_noise_free_list, '--s', label = 'noise-free simulator', markerfacecolor='none')
        plt.plot(layers_list_plot, tf_list, 'k--')
        plt.legend(loc = 'lower right')

    plt.tight_layout()
    out_file = f'plot/qbit{qdim}_device{device_type}_layers{layers}.pdf'
    print("[INFO] Saving result in", out_file)
    plt.savefig(out_file)
    # plt.show()


if __name__ == "__main__":

    qdim = 1
    rank =4
    an = 3
    layers = 3
    device_type = 'sim'
    # device_type = 'real'
    noise_mdl = 'simulator'
    total_chan_no = 100   
    
    if len(sys.argv) != 2:
        print("Usage", sys.argv[0], "`type`")
        print("`type` can be `single` or `average`")
        sys.exit(-1)
    else :
        if sys.argv[1] == 'single' :
            # fidelity plot for one channel
            noise_amp_list = [0, 0.05, 0.2, 0.5, 1]
            single_chan_fidelity(qdim, rank, an, layers, device_type, noise_amp_list)
        if sys.argv[1] == 'average' :
            # fidelity average error over more than one channel
            average_fidelity(qdim, rank, an, noise_mdl, total_chan_no)
 
