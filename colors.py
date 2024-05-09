import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_color_distribution(frame):
    # Reshape the frame to be a 2D array of pixels
    pixels = frame.reshape(-1, 3)
    
    # Use numpy to count the occurrences of each color
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Normalize the counts to get a distribution
    distribution = counts / np.sum(counts)
    
    return unique_colors, distribution

def plot_color_distribution(unique_colors, distribution):
    # Plot the color distribution
    plt.figure(figsize=(10, 5))
    plt.bar(unique_colors[:,0], distribution, width=0.01)
    plt.xlabel('Color')
    plt.ylabel('Distribution')
    plt.title('Color Distribution of Video Frame')
    plt.show()

def main():
    # Open the video file
    video_path = './videos/alumin.mp4'
    cap = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return
    
    # Read and process each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate color distribution for the current frame
        unique_colors, distribution = calculate_color_distribution(frame)
        
        # Plot the color distribution
        plot_color_distribution(unique_colors, distribution)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()