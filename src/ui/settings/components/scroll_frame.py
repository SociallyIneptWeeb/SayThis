import tkinter as tk
from tkinter import ttk


class ScrollFrame(ttk.Frame):
    """A scrollable frame component that can contain other widgets."""
    
    def __init__(self, parent):
        """Initialize the scrollable frame.
        
        Args:
            parent: The parent widget to contain this component
        """
        super().__init__(parent)  # create a frame (self)

        # Place canvas on self
        self.canvas = tk.Canvas(self)
        # Place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = ttk.Frame(self.canvas)
        # Place a scrollbar on self
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        # Attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Pack scrollbar to right of self
        self.vsb.pack(side="right", fill="y")
        # Pack canvas to left of self and expand to fill
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw", tags="self.viewPort")

        # Bind an event whenever the size of the viewPort frame changes
        self.viewPort.bind("<Configure>", self.on_frame_configure)
        # Bind an event whenever the size of the canvas changes
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.on_frame_configure(None)

        # Bind mouse wheel events
        self.viewPort.bind('<Enter>', self._bound_to_mousewheel)
        self.viewPort.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        """Bind mousewheel events when mouse enters the viewport."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        """Unbind mousewheel events when mouse leaves the viewport."""
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        # Whenever the size of the frame changes, alter the scroll region respectively
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Reset the canvas window to encompass inner frame when required."""
        canvas_width = event.width
        # Whenever the size of the canvas changes alter the window region respectively
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
