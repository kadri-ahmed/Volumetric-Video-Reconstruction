import pandas as pd
import plotly.express as px

csv_file_path_1 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\small_mesh_reading.csv"
csv_file_path_2 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\big_mesh_reading.csv"
csv_file_path_3 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\small_mesh_compression.csv"
csv_file_path_4 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\big_mesh_compression.csv"
csv_file_path_5 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\track_copy_data_time.csv"
csv_file_path_6 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\track_loading_texture_time.csv"
csv_file_path_7 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\track_loading_time.csv"
csv_file_path_8 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\total_loading_time.csv"

csv_file_path_9 = "C:\\Users\\ahmed\Documents\\4D-VRmovie\\benchmarks\\compare_simplified_vs_dense_wtex_compressed.csv"

df = pd.read_csv(csv_file_path_9)

fig = px.line(df,
    x = 'FrameIndex',
    y = ['Dense model(ms)','Simplified model(ms)'],
    width=700, 
    height=500,
    template='plotly_dark'
)
            
fig.show()