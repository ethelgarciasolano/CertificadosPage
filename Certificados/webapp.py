from . import app  # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.
import sys

print('hi', file=sys.stderr)