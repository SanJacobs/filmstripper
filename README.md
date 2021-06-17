# Filmstripper
A tool for fusing multiple images together into a single filmstrip.

## Usage

Filmstripper takes a folder as input and a file-path as output. It can generate both vertical and horizontal filmstrips, the choice is made by either writing `v` for vertical, or `h` for horizontal. Vertical is the default, if nothing else is chosen.

```
python3 filmstripper.py /input/directory/ /output/file.png [v/h]
```

## Examples

Starting out with a png image sequence like this in a folder:

![image](https://user-images.githubusercontent.com/21090839/110244138-ab721a80-7f5d-11eb-81a8-759f8e894ed6.png)


Will generate one png like this:

![Slider_Large](https://user-images.githubusercontent.com/21090839/110244156-bd53bd80-7f5d-11eb-89ba-465416a838f4.png)

This one was generated with the `h` argument, so it is horizontal, rather than vertical.
