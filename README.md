# Realtime Digital Filter Design Application

This desktop application provides a user-friendly interface for designing custom digital filters through zeros-poles placement on the z-plane. Users can manipulate filter elements, visualize frequency responses, apply filters in real-time, and correct phase with added All-Pass filters. The application aims to simplify the filter design process with intuitive controls and interactive features.

## Demo

![Demo](Demo.gif)


## Running the Application

To run the application, follow these steps:

1. Ensure you have Python installed on your system (version X.X.X recommended).
2. Clone this repository to your local machine.
3. Install the required dependencies by running the following command in your terminal or command prompt:

```bash
pip install scipy
```

4. Run the application script:

```bash
python Application1.py
```

The application window will appear, providing access to the various design and visualization features.

## Features

### Z-Plane Visualization
- Interactive plot of the z-plane with the unit circle.
- Place, modify, and delete zeros and poles by dragging or clicking.
- Clear individual zeros, poles, or all elements.
- Option to add or omit conjugates for complex elements.

### Frequency Response Visualization
- Graphs depicting magnitude and phase responses for the placed elements.

### Real-Time Filtering
- Apply the designed filter on a lengthy signal in real-time.
- Dynamic graph displaying time progress of the original and filtered signals.
- Control the filtering speed/temporal-resolution via a slider.
- Input arbitrary real-time signals by moving the mouse in a designated area.

### All-Pass Filters
- Library of pre-built All-Pass filters with visualizations of zero-pole combinations and phase responses.
- Select and add All-Pass filters to the original design.
- Create custom All-Pass filters by specifying an arbitrary "a" value, with automatic phase response calculation and integration into the library.
- Enable/disable added All-Pass elements via a drop-down menu or checkboxes.
