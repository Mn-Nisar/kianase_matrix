import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_matrix_plot(main_data_df,color_data_df):
    color_mapping = {
        color_data_df.iat[i, j]: tuple(int(color_data_df.iat[i,
    j][1:][k:k+2], 16) for k in (0, 2, 4))
        for i in range(color_data_df.shape[0])
        for j in range(color_data_df.shape[1])
    }

    main_data_array = main_data_df.to_numpy()

    rgb_data = np.array([[color_mapping[color_data_df.iat[i, j]] for j in
    range(main_data_df.shape[1])]
                        for i in range(main_data_df.shape[0])], dtype=np.uint8)

    fig, ax = plt.subplots()
    heatmap = ax.imshow(rgb_data)

    # for i in range(main_data_df.shape[0]):
    #     for j in range(main_data_df.shape[1]):
    #         text = ax.text(j, i, main_data_df.iat[i, j], ha='center',
    # va='center', color='black')
    
    ax.xaxis.tick_top()
    
    ax.set_xlabel('Phosposites')
    ax.set_ylabel('Phosposites')
   
    ax.xaxis.set_label_position('top') 

    ax.set_xticks(np.arange(main_data_df.shape[1]))
    ax.set_yticks(np.arange(main_data_df.shape[0]))
    ax.set_xticklabels(main_data_df.columns , rotation = 90)
    ax.set_yticklabels(main_data_df.index)

    plt.show()
