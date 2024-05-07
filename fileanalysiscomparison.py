import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from scipy.stats import pearsonr

def load_and_extract_features(file_path):
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)
    # Extract features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    harmonic, percussive = librosa.effects.hpss(y)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=harmonic, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    return mfccs, harmonic, percussive, spectral_contrast, chroma, tonnetz, sr

def compute_similarity(features1, features2):
    # Calculate distances
    mfcc_distance = np.linalg.norm(np.mean(features1['mfccs'], axis=1) - np.mean(features2['mfccs'], axis=1))
    chroma_distance = np.linalg.norm(np.mean(features1['chroma'], axis=1) - np.mean(features2['chroma'], axis=1))

    # Normalize each distance independently
    max_mfcc = max(mfcc_distance, 1)  # Use 1 as a fallback to prevent division by zero
    max_chroma = max(chroma_distance, 1)  # Use 1 as a fallback to prevent division by zero

    scores = {
        'mfcc_distance': mfcc_distance / max_mfcc,
        'chroma_distance': chroma_distance / max_chroma,
    }

    # Calculate and directly assign correlation scores
    scores['spectral_contrast_corr'] = pearsonr(np.mean(features1['spectral_contrast'], axis=1), np.mean(features2['spectral_contrast'], axis=1))[0]
    scores['tonnetz_corr'] = pearsonr(np.mean(features1['tonnetz'], axis=1), np.mean(features2['tonnetz'], axis=1))[0]

    return scores





def plot_features(mfccs1, mfccs2, harmonic1, harmonic2, spectral_contrast1, spectral_contrast2, chroma1, chroma2, tonnetz1, tonnetz2, sr, title1, title2):
    plt.figure(figsize=(20, 15))

    # MFCCs
    plt.subplot(4, 2, 1)
    librosa.display.specshow(mfccs1, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title(f'MFCCs of {title1}')
    plt.subplot(4, 2, 2)
    librosa.display.specshow(mfccs2, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title(f'MFCCs of {title2}')

    # Harmonic waveforms using plt.plot instead of waveshow
    plt.subplot(4, 2, 3)
    plt.plot(np.linspace(0, len(harmonic1) / sr, num=len(harmonic1)), harmonic1, alpha=0.5)
    plt.title(f'Harmonic of {title1}')
    plt.subplot(4, 2, 4)
    plt.plot(np.linspace(0, len(harmonic2) / sr, num=len(harmonic2)), harmonic2, alpha=0.5)
    plt.title(f'Harmonic of {title2}')

    # Spectral Contrast
    plt.subplot(4, 2, 5)
    librosa.display.specshow(spectral_contrast1, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title(f'Spectral Contrast of {title1}')
    plt.subplot(4, 2, 6)
    librosa.display.specshow(spectral_contrast2, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title(f'Spectral Contrast of {title2}')

    # Chroma
    plt.subplot(4, 2, 7)
    librosa.display.specshow(chroma1, x_axis='time', y_axis='chroma', sr=sr)
    plt.colorbar()
    plt.title(f'Chroma of {title1}')
    plt.subplot(4, 2, 8)
    librosa.display.specshow(chroma2, x_axis='time', y_axis='chroma', sr=sr)
    plt.colorbar()
    plt.title(f'Chroma of {title2}')

    plt.tight_layout()
    plt.savefig('feature_plots.png')  # Save the plot as a PNG file instead of showing it
    plt.close()  # Close the plot to free up memory and avoid display

def plot_similarity_scores(scores):
    labels = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, values, color='skyblue', alpha=0.7)

    for bar, value in zip(bars, values):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{value:.2f}", ha='center', va='bottom')

    plt.ylim(0, 1.1)  # Set y-axis limits from 0 to just above the highest value (normalized)
    plt.ylabel('Normalized Scores')
    plt.title('Similarity Scores Comparison')
    plt.savefig('similarity_scores_normalized.png')
    plt.close()




def main():
    original_path = 'N:\\ChordExtract Test\\Lana Del Rey - Summertime Sadness (Lyrics).mp3'
    backing_path = 'N:\\ChordExtract Test\\lanabacking.mp3'

    # Load and extract features
    mfccs_original, harmonic_original, percussive_original, spectral_contrast_original, chroma_original, tonnetz_original, sr = load_and_extract_features(original_path)
    mfccs_backing, harmonic_backing, percussive_backing, spectral_contrast_backing, chroma_backing, tonnetz_backing, _ = load_and_extract_features(backing_path)

    # Compute similarity
    features_original = {'mfccs': mfccs_original, 'chroma': chroma_original, 'spectral_contrast': spectral_contrast_original, 'tonnetz': tonnetz_original}
    features_backing = {'mfccs': mfccs_backing, 'chroma': chroma_backing, 'spectral_contrast': spectral_contrast_backing, 'tonnetz': tonnetz_backing}
    similarity_scores = compute_similarity(features_original, features_backing)

    # Plotting the features and saving them
    plot_features(mfccs_original, mfccs_backing, harmonic_original, harmonic_backing, spectral_contrast_original, spectral_contrast_backing, chroma_original, chroma_backing, tonnetz_original, tonnetz_backing, sr, 'Original Track', 'Backing Track')
    
    # Plotting and saving the similarity scores
    plot_similarity_scores(similarity_scores)
    

if __name__ == "__main__":
    main()


