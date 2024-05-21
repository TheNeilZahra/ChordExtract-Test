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
    scores = {}
    # Euclidean distance for MFCCs and Chroma
    mfcc_distance = np.linalg.norm(np.mean(features1['mfccs'], axis=1) - np.mean(features2['mfccs'], axis=1))
    chroma_distance = np.linalg.norm(np.mean(features1['chroma'], axis=1) - np.mean(features2['chroma'], axis=1))
    
    # Normalize distances
    max_distance = max(mfcc_distance, chroma_distance)
    scores['mfcc_distance'] = mfcc_distance / max_distance
    scores['chroma_distance'] = chroma_distance / max_distance

    # Correlation for Spectral Contrast and Tonnetz (normalized to be between 0 and 1)
    scores['spectral_contrast_corr'] = (pearsonr(np.mean(features1['spectral_contrast'], axis=1), np.mean(features2['spectral_contrast'], axis=1))[0] + 1) / 2
    scores['tonnetz_corr'] = (pearsonr(np.mean(features1['tonnetz'], axis=1), np.mean(features2['tonnetz'], axis=1))[0] + 1) / 2

    return scores


def plot_features_and_scores(mfccs1, mfccs2, harmonic1, harmonic2, spectral_contrast1, spectral_contrast2, chroma1, chroma2, tonnetz1, tonnetz2, sr, scores, title1, title2):
    plt.figure(figsize=(20, 20))  # Increase figure size for better readability

    # Plot MFCCs
    ax1 = plt.subplot(4, 2, 1)
    librosa.display.specshow(mfccs1, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title(f'MFCCs of {title1}')
    ax2 = plt.subplot(4, 2, 2)
    librosa.display.specshow(mfccs2, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title(f'MFCCs of {title2}')

    # Annotate MFCC Distance
    ax1.text(0.5, 1.05, f"MFCC Distance: {scores['mfcc_distance']:.2f}", size=12, ha="center", transform=ax1.transAxes)
    ax2.text(0.5, 1.05, f"MFCC Distance: {scores['mfcc_distance']:.2f}", size=12, ha="center", transform=ax2.transAxes)

    # Plot Harmonic waveforms
    plt.subplot(4, 2, 3)
    plt.plot(np.linspace(0, len(harmonic1)/sr, num=len(harmonic1)), harmonic1, alpha=0.5)
    plt.title(f'Harmonic of {title1}')
    plt.subplot(4, 2, 4)
    plt.plot(np.linspace(0, len(harmonic2)/sr, num=len(harmonic2)), harmonic2, alpha=0.5)
    plt.title(f'Harmonic of {title2}')

    # Plot Spectral Contrast
    ax3 = plt.subplot(4, 2, 5)
    librosa.display.specshow(spectral_contrast1, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title(f'Spectral Contrast of {title1}')
    ax4 = plt.subplot(4, 2, 6)
    librosa.display.specshow(spectral_contrast2, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title(f'Spectral Contrast of {title2}')

    # Annotate Spectral Contrast Correlation
    ax3.text(0.5, -0.15, f"Spectral Contrast Correlation: {scores['spectral_contrast_corr']:.2f}", size=12, ha="center", transform=ax3.transAxes)
    ax4.text(0.5, -0.15, f"Spectral Contrast Correlation: {scores['spectral_contrast_corr']:.2f}", size=12, ha="center", transform=ax4.transAxes)

    # Plot Chroma
    plt.subplot(4, 2, 7)
    librosa.display.specshow(chroma1, x_axis='time', y_axis='chroma', sr=sr)
    plt.colorbar()
    plt.title(f'Chroma of {title1}')
    plt.subplot(4, 2, 8)
    librosa.display.specshow(chroma2, x_axis='time', y_axis='chroma', sr=sr)
    plt.colorbar()
    plt.title(f'Chroma of {title2}')

    plt.tight_layout(pad=2.0)  # Adjust layout to prevent overlap
    plt.show()



    


def main():
    original_path = 'N:\ChordExtract Test\Lana Del Rey - Summertime Sadness (Lyrics).mp3'
    backing_path = 'N:\ChordExtract Test\lanabacking.mp3'

    # Load and extract features
    mfccs_original, harmonic_original, percussive_original, spectral_contrast_original, chroma_original, tonnetz_original, sr = load_and_extract_features(original_path)
    mfccs_backing, harmonic_backing, percussive_backing, spectral_contrast_backing, chroma_backing, tonnetz_backing, _ = load_and_extract_features(backing_path)

    # Compute similarity
    features_original = {'mfccs': mfccs_original, 'chroma': chroma_original, 'spectral_contrast': spectral_contrast_original, 'tonnetz': tonnetz_original}
    features_backing = {'mfccs': mfccs_backing, 'chroma': chroma_backing, 'spectral_contrast': spectral_contrast_backing, 'tonnetz': tonnetz_backing}
    similarity_scores = compute_similarity(features_original, features_backing)

    # Plotting the features and scores
    plot_features_and_scores(mfccs_original, mfccs_backing, harmonic_original, harmonic_backing, spectral_contrast_original, spectral_contrast_backing, chroma_original, chroma_backing, tonnetz_original, tonnetz_backing, sr, similarity_scores, 'Original Track', 'Backing Track')
    
    # Display similarity scores
    print("Similarity Scores:")
    for key, value in similarity_scores.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
