"""Build, tag and push a docker image from a Dockerfile.

Builds the image found in the work directory, tags it against every
registry base in config.py's DOCKER_DTR_BASE with "latest" and the
current date (plus any additional tags), and pushes all of them.
"""
import sys
from ImageBuilder import ImageBuilder


if __name__ == "__main__":
  args = ImageBuilder.parse_args(system_args=sys.argv[1:])
  builder = ImageBuilder(
    work_dir=args.work_dir,
    dockerfile=args.file,
    debug=args.debug,
    additional_tags=args.tags
  )
  print(builder)
  new_image = builder.build_image()
  builder.tag_image(target_image=new_image)
  builder.show_built_image(target_image=new_image)
  builder.push_image()
