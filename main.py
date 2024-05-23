from ntcore.ntcore import NTCore, NetworkTablesType

# Get or create the NT client instance
ntcore_instance = NTCore.get_instance_by_team(973)

# Create the autoMode topic w/ a default return value of 'No Auto'
auto_mode_topic = ntcore_instance.create_topic('/MyTable/autoMode', NetworkTablesType.STRING, 'No Auto')

# Publish the topic
auto_mode_topic.publish()

# Set a new value
auto_mode_topic.set_value('25 Ball Auto and Climb')