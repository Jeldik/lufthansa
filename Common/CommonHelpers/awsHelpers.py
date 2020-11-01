import json
import logging as logger
import config
import paho.mqtt.client as mqtt


class AwsHelpers:
    CONNECTED_CODE = 0
    SUCCESS_CODE = 200
    DEPARTURE_MESSAGE = 'New Estimated Departure'
    ARRIVAL_MESSAGE = 'New Estimated Arrival'
    queue = {}

    def __init__(self, context):
        self.context = context

    def on_connect(self, client, userdata, flags, rc):
        if rc == self.CONNECTED_CODE:
            logger.info("Connected to broker")
            client.subscribe(config.APICONFIG['topic'])
        else:
            logger.info("Failed to connect, return code {}\n", rc)

    def on_message(self, client, userdata, msg):
        if len(self.queue) != 0:
            self.context.execute_steps(u"""
            When I request flight status from API
            And go to lufthansa website
            And confirm privacy settings
            And I click to flight status
            And enter data from API
            Then data should be the same
            """)
        logger.info(msg.topic + " " + msg.payload.decode())
        msg_data = json.loads(msg.payload.decode())
        message = msg_data['Update']['Message']

        if (self.ARRIVAL_MESSAGE in message or self.DEPARTURE_MESSAGE in message) and 'LH' in msg_data['Update']['FlightNumber']:
            flight_number = msg_data['Update']['FlightNumber']
            event = msg_data['Update']['Message']
            self.queue[flight_number] = event
            self.context.queue = self.queue

        return

    def run(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.tls_set(config.APICONFIG['ca_file'], config.APICONFIG['certificate_file'], config.APICONFIG['key_file'])
        client.connect(config.APICONFIG['broker'], config.APICONFIG['port_broker'])
        client.loop_forever()
