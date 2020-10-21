import os

def get_output(sample_index):

    output_file = 'nats_output_{}.txt'.format(sample_index)

    print('get_output:', os.path.abspath(output_file))
    with open(output_file,'r') as f:
        val = float(f.readline().strip())

    return val

def calc_sep_distance_vs_time(df):
    """Compute separation distance vs time for two aircraft

    Parameters
    ----------
    df : DataFrame
        DataFrame obtained from reading NATS simulation results.
        Simulation results should contain data for two aircraft
    
    Returns
    -------
    DataFrame
        DataFrame with time as index and 'sep' column for separation
        distance
    """
    callsigns = df['callsign'].unique()
    def extract_single_ac_data(callsign):
        return df.loc[df['callsign'] == callsign, ['time','latitude','longitude']].set_index('time').resample('1T').mean()
    df1 = extract_single_ac_data(callsigns[0])
    df2 = extract_single_ac_data(callsigns[1])

    new_df = df1.merge(df2, left_index=True, right_index=True)
    # Todo: use a better separation distance calculation.  This is just an L2 distance of the lat/long, but may be better to first compute a projection of the coordinates
    new_df['sep'] = new_df.apply(lambda row: np.sqrt((row['latitude_x'] - row['latitude_y'])**2 + (row['longitude_x'] - row['longitude_y'])**2), axis=1)

    return new_df