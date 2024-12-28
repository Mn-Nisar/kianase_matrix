import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.colors import LinearSegmentedColormap


def get_matrix_plot(main_data_df,color_data_df,kianase,type_):
    color_mapping = {
        color_data_df.iat[i, j]: tuple(int(color_data_df.iat[i,
    j][1:][k:k+2], 16) for k in (0, 2, 4))
        for i in range(color_data_df.shape[0])
        for j in range(color_data_df.shape[1])
    }

    main_data_array = main_data_df.to_numpy()
    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)

    rgb_data = np.array([[color_mapping[color_data_df.iat[i, j]] for j in
    range(main_data_df.shape[1])]
                        for i in range(main_data_df.shape[0])], dtype=np.uint8)

    c = ["#0F6D37","#1D8F4E","#31AF68","#70DC9F","#FFFFFF", "#EA7F7F","#E01919","#A52222","#751818","#4D0808"]
    v = [0,.10,.15,.4,.5,0.6,.8,.9,1.]
    l = list(zip(v,c))
    cmap=LinearSegmentedColormap.from_list('rg',l, N=256)
    heatmap = ax.imshow(rgb_data,cmap=cmap)

    # fig, ax = plt.subplots()
    heatmap = ax.imshow(rgb_data,cmap=cmap)

    # for i in range(main_data_df.shape[0]):
    #     for j in range(main_data_df.shape[1]):
    #         if main_data_df.iat[i, j] != 0:
    #             text = ax.text(j, i, main_data_df.iat[i, j], ha='center',
    # va='center', color='black',fontsize=5)
    
    ax.xaxis.tick_top()
    
    ax.set_xlabel(f'{kianase} Phosphosites',fontsize=6)
    ax.set_ylabel(f'{kianase} Phosphosites',fontsize=6)
   
    ax.xaxis.set_label_position('top') 

    ax.set_xticks(np.arange(main_data_df.shape[1]))
    ax.set_yticks(np.arange(main_data_df.shape[0]))
    ax.set_xticklabels(main_data_df.columns , rotation = 90,fontsize=5)
    ax.set_yticklabels(main_data_df.index,fontsize=5)

    cbar_ax = fig.add_axes([0.82, 0.17, 0.02, 0.6])
    # fig.colorbar(heatmap, cax=cbar_ax)
    cbar = fig.colorbar(heatmap, cax=cbar_ax)
    cbar_ax.set_yticks([])
    cbar_ax.set_yticklabels([])

    plt.title("Co-upregulated",fontsize=6,rotation=360)
    plt.ylabel("Expression", fontsize=6, rotation=90, labelpad=-30)
    plt.xlabel("Co-downregulated",fontsize=6,rotation=360)
   
   
    plt.tight_layout(pad=1.2)
    plt.savefig(f'output/{kianase}_{type_}_plot.svg',format='svg')
    
