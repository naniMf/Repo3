import pandas as pd
import numpy as np


def MAE():
    sigma = 0
    n = sum(list(before_noise.values()))
    for bin in before_noise:
        true = before_noise[bin]
        noisy = unique_noisy_bins.get(bin)
        if noisy:
            sigma = abs(noisy - true)

    return round(sigma / n, 7)


df = pd.read_csv(r'adult_age_gender_dataset.csv')
# add_noise_to_age = False


before_noise = {}  # dictionary to store bins with the frequency
noisy_df = list()  # list of dataframes to store noisy bins

# enumerate over all possible ages and genders
for noise_target in [False]:
    if noise_target:
        noise_target_str = '"Age" IS noisy'
    else:
        noise_target_str = '"Age" IS NOT noisy'
    for epsilon in [0.001,0.01, 0.1, 1, 10]:
        before_noise = {}  # dictionary to store bins with the frequency
        noisy_df = list()  # list of dataframes to store noisy bins
        for age in range(17, 95):
            for gender in [1, 2]:
                # find unique bins as a dataframe
                selected_df = df[(df['Age'] == age) & (df['Gender'] == gender)]
                # store original bins before adding noise

                if len(selected_df) > 0:
                    before_noise[str((age, gender))] = len(selected_df)
                    # record count in each unique bin
                    data_count = selected_df.shape[0]
                    print("Data count: ", data_count)

                    # add noise to each element of the unique bin
                    for i in range(len(selected_df)):
                        # calculate the laplacian noise
                        noise = np.random.laplace(loc=0, scale= 1/epsilon)

                        # check the noise value, if it is zero and round all to the nearest integer
                        if noise < 0:
                            noise = 0
                        noise = round(noise)
                        # Check if should add noise to 'Gender' as well or only 'Age'
                        if noise_target:
                            selected_df.iloc[i, :] = selected_df.iloc[i, :].add(noise)
                        else:
                            selected_df.iloc[i, 0] = selected_df.iloc[i, 0] + noise
                    noisy_df.append(selected_df)
                else:
                    print(str((age, gender)))
                print('End loop')

        # concatenate unique bins (dataframes)
        print('concatenate unique bins (dataframes)')
        noisy_dfs = pd.concat(noisy_df)

        # find unique bins after adding noise
        unique_noisy_bins = {}
        for j,age in enumerate(range(noisy_dfs['Age'].min(), noisy_dfs['Age'].max())):
            for gender in list(set(noisy_dfs['Gender'].values)):
                unique_noisy_bin = noisy_dfs[(noisy_dfs['Age'] == age) & (noisy_dfs['Gender'] == gender)]
                if len(unique_noisy_bin) > 0:
                    unique_noisy_bins[str((age, gender))] = len(unique_noisy_bin)

        print('Total number of bins BEFORE Adding noise (%s):' % noise_target_str, len(before_noise))
        print('Total number of bins AFTER Adding noise (%s):' % noise_target_str, len(unique_noisy_bins))
        print("MAE (epsilon=%s): " % str(epsilon), MAE())
        print('Storing results')
        with open('noise2.txt', 'a') as f:
            f.write('Total number of bins BEFORE Adding noise (%s):' % noise_target_str + ' ' + str(len(before_noise)))
            f.write('\n')
            f.write(
                'Total number of bins AFTER Adding noise (%s):' % noise_target_str + ' ' + str(len(unique_noisy_bins)))
            f.write('\n')
            f.write('"MAE (epsilon=%s): "' % str(epsilon) + ' ' + str(MAE()))
            f.write('\n')
        print('Write finished')
