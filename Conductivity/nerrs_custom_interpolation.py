import pandas as pd
import numpy as np
from datetime import timedelta
import os

def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['timestamp'])
    df.sort_values('timestamp', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def compute_weekly_mean(df, gap_start, gap_end):
    week_before = (gap_start - timedelta(days=7), gap_start)
    week_after = (gap_end, gap_end + timedelta(days=7))
    
    before_mean = df[(df['timestamp'] >= week_before[0]) & (df['timestamp'] < week_before[1])]['salinity'].mean()
    after_mean = df[(df['timestamp'] > week_after[0]) & (df['timestamp'] <= week_after[1])]['salinity'].mean()
    
    if np.isnan(before_mean) or np.isnan(after_mean):
        overall_mean = df['salinity'].mean()
        return overall_mean, overall_mean
    return before_mean, after_mean

def extract_variation(df, start_time, window_hours=12):
    end_time = start_time - timedelta(days=7)
    period_data = df[(df['timestamp'] >= end_time) & (df['timestamp'] < start_time)].copy()
    period_data = period_data.dropna(subset=['salinity'])

    if len(period_data) < 2:
        return np.zeros(window_hours*2)

    # Interpolate to get even hourly values (2 per hour for 30-min interval)
    period_data.set_index('timestamp', inplace=True)
    resampled = period_data['salinity'].resample('30T').mean().interpolate()
    values = resampled[-(window_hours * 2):]  # Last 12 hours
    baseline = values.mean()
    return values - baseline

def fill_missing_with_trend_and_variation(df):
    filled_df = df.copy()
    gap_indices = filled_df[filled_df['salinity'].isna()].index

    mean_records = []
    variation_records = []

    # Identify contiguous NaN blocks
    blocks = []
    current_block = []
    for idx in gap_indices:
        if not current_block or idx == current_block[-1] + 1:
            current_block.append(idx)
        else:
            blocks.append(current_block)
            current_block = [idx]
    if current_block:
        blocks.append(current_block)

    for block in blocks:
        start_idx, end_idx = block[0], block[-1]
        gap_start, gap_end = filled_df.loc[start_idx, 'timestamp'], filled_df.loc[end_idx, 'timestamp']
        
        # Mean
        start_mean, end_mean = compute_weekly_mean(df, gap_start, gap_end)
        time_range = (gap_end - gap_start).total_seconds() / 3600
        time_steps = np.linspace(0, 1, len(block))

        # Linear interpolation
        linear_interp = start_mean + time_steps * (end_mean - start_mean)

        # Store mean points
        mean_records.append({'timestamp': gap_start, 'mean_salinity': start_mean})
        mean_records.append({'timestamp': gap_end, 'mean_salinity': end_mean})

        # Get 12-hour variation
        variation = extract_variation(df, gap_start)
        variation_steps = np.resize(variation.values, len(block))

        # Store variation for export
        for i, step_val in enumerate(variation_steps):
            variation_records.append({'step': i, 'variation': step_val})

        # Apply variation
        filled_values = linear_interp + variation_steps
        filled_df.loc[block, 'salinity'] = filled_values

    # Save outputs
    pd.DataFrame(mean_records).drop_duplicates().to_csv("mean_salinity_points.csv", index=False)
    pd.DataFrame(variation_records).to_csv("daily_variations.csv", index=False)
    filled_df.to_csv("interpolated_salinity.csv", index=False)

    return filled_df

# Main program
def main():
    file_path = "your_data.csv"  # Replace with your file name
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    df = load_data(file_path)
    filled_df = fill_missing_with_trend_and_variation(df)
    print("Interpolation complete. Output saved as:")
    print("- mean_salinity_points.csv")
    print("- daily_variations.csv")
    print("- interpolated_salinity.csv")

if __name__ == "__main__":
    main()
