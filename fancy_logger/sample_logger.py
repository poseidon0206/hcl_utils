from fancy_logger import FancyLogger, TermColors


_logger = FancyLogger(caller=__name__).get_logger()
log_colors = TermColors()


_logger.info("this is an info message.")
_logger.warning("Here's a warning, you've been warned.")
_logger.error("THIS IS AN ERROR MESSAGE IN CAPS!")
_logger.debug("This debug message shouldn't be shown in the dfault logging level.")

_logger.info(f"{log_colors.blue}this message is in blue.{log_colors.none}")
_logger.warning(f"{log_colors.yellow}this warning is in yellow.{log_colors.none}")
_logger.error(f"{log_colors.red}this error is in red.{log_colors.none}")

# setting logging level to debug
_logger.setLevel(10)
_logger.debug("This debug message will be shown now the debug level is low enough.")
