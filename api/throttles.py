from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class BurstUserRateThrottle(UserRateThrottle):
	scope = 'burst_user'


class SustainedUserRateThrottle(UserRateThrottle):
	scope = 'sustained_user'


class BurstAnonRateThrottle(AnonRateThrottle):
	scope = 'burst_anon'


class SustainedAnonRateThrottle(AnonRateThrottle):
	scope = 'sustained_anon'
