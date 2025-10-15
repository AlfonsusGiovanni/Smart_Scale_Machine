import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automatic_scale_machine import weight_rounder as wr

wr.Mysetting.process_value(50.12)