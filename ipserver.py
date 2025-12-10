import asyncio
import time

from zeroconf import (
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf,
)

class Ipserver():
	
	WAITING_TIME = 10
	__url = None
		
	def __init__(self, service, handler):
		
		self.__service = service
		self.zeroconf = Zeroconf()
		print(f"\nBrowsing service...")
		browser = ServiceBrowser(self.zeroconf, [service], handlers=[self.__on_service_state_change])
		asyncio.create_task(self.__loop(handler))

	def __on_service_state_change(
			self,
			zeroconf: Zeroconf, 
			service_type: str, 
			name: str, 
			state_change: ServiceStateChange
			) -> None:
   
		print("on_service_state_change : " + str(name))
		info = zeroconf.get_service_info(service_type, name)
		addr = info.parsed_scoped_addresses()[0] + ':' + str(info.port)
		
		if service_type == self.__service:
				self.__url = addr

	async def __loop(self,handler):
		
		end_time = time.time() + self.WAITING_TIME

		while self.__url ==  None:
			await asyncio.sleep(0.2)
			if time.time() > end_time:
				break

		self.zeroconf.close()
		handler(self.__url)



		
