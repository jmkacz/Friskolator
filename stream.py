import os

#defines info for collecting data from flickr
user_id = "81953314@N02"
event_tag = "prehope_test"

#data directory
project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
event_data_dir = os.path.join(
    project_path,
    "Friskolator_data",
    event_tag
)

#template for a frisk event 
# Must match data outline in Friskolator_data/README.md 
# for this to work
template_frisk = {
    "version":"0.5", # cur version of this template
    "event": event_tag,
    "constented":True,
    "metadata": {},
}
