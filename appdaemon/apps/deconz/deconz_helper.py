import appdaemon.plugins.hass.hassapi as hass
import datetime
from datetime import datetime

class DeconzHelper(hass.Hass):

  def initialize(self) -> None:
    self.listen_event(self.event_received, "deconz_event")
    for sensor in self.args["motions"]:
      # self._check_entity(entity=sensor, namespace=sensor.split('.')[0])
      self.listen_state(self.motion_listener, sensor)
      self.log(f"State listener set for {sensor}")

  def event_received(self, event_name, data, kwargs):
    if data != {}:
      event_data = data["event"]
      event_id = data["id"]
      event_received = datetime.now()

      self.log("Deconz event received from {}. Event was: {}".format(event_id, event_data))
      # self.set_state("sensor.deconz_event", state = event_id, attributes = {"event_data": event_data, "event_received": str(event_received)})

      if data['id'] == self.args['switch_1_id']:
        self.log(data['event'])
        if data['event'] == 1000:
          self.log('Button down')
        elif data['event'] == 1001:
          self.log('Button long click down')
        elif data['event'] == 1002:
          self.log('Button release')
        elif data['event'] == 1003:
          self.log('Button long click release')
        elif data['event'] == 1004:
          self.log('Button double click')
        elif data['event'] > 1004 and data['event'] < 1010:
          self.log('Button multi click')
        else:
          self.log('Event not suported')
    else:
      self.log('Data is empty')

  def motion_listener(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.log(f"Motion detected in {self.friendly_name(entity)} and attributets {attribute}")