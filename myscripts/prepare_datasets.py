#!/usr/bin/env python3
import os
import pandas as pd

# Initialize relevant strings
apps = 'blockscholes bodytrack freqmine kmeans stereomatch swaptions'.split()
apps = ['blockscholes']  # TODO
base_folder = os.path.join('..', 'inputs', 'agora')

for app in apps:
  print("\n", ">>>>>", app)
  app_folder = os.path.join(base_folder, app)
  full_dataset_app_folder = os.path.join(app_folder, 'full')
  if not os.path.isdir(full_dataset_app_folder):
    os.mkdir(full_dataset_app_folder)

  # Set maximum number of iteration of this app
  maxiter = 100 if app == 'stereomatch' else 40
  listdir = os.listdir(app_folder)

  # Loop over files of different iterations
  for it in range(1, maxiter+1):
    covariate_file = f'data_itr_{it}.csv'
    target_file = f'target_exec_time_ms_itr_{it}.csv'

    # Check whether the two files actually exist
    if not (covariate_file in listdir and target_file in listdir):
      exit(f"Error: {covariate_file} or {target_file} does not exist")
    covariate_file_path = os.path.join(app_folder, covariate_file)
    target_file_path = os.path.join(app_folder, target_file)

    # Join covariates and target into a single, full dataset
    df = pd.read_csv(covariate_file_path, encoding='utf-8')
    df_tar = pd.read_csv(target_file_path, encoding='utf-8')
    df['exec_time_ms'] = df_tar['exec_time_ms']

    # Save new dataset to file
    df_path = os.path.join(full_dataset_app_folder, f'itr{it}.csv')
    df.to_csv(df_path, index=False)
    print(f"Successfully saved to {df_path}")
