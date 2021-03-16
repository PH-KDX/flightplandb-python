#!/usr/bin/env python3

from typing import List, Union, Optional
from dataclasses import dataclass, fields
from dateutil.parser import isoparse
from datetime import datetime
from enum import Enum, EnumMeta, auto


@dataclass
class StatusResponse:
    """
    Returned for some functions to indicate execution status

    Attributes
    ----------
    message : str
        The message associated with the status returned
    errors : Union[List[str], None]
        A list of any errors raised
    """
    message: str
    errors: Union[List[str], None]


@dataclass
class User:
    """Describes users registered on the website

    Attributes
    ----------
    id : int
        Unique user identifier number
    username : str
        Username
    location : Optional[Union[str, None]]
        User provided location information. ``None`` if not available
    gravatarHash : Optional[str]
        Gravatar hash based on user's account email address.
    joined : Optional[datetime] = None
        UTC Date and time of user registration
    lastSeen : Optional[datetime] = None
        UTC Date and time the user was last connected
    plansCount : Optional[int]
        Number of flight plans created by the user
    plansDistance : Optional[float]
        Total distance of all user's flight plans
    plansDownloads : Optional[int]
        Total download count of all user's plans
    plansLikes : Optional[int]
        Total like count of all user's plans
    """
    id: int
    username: str
    location: Optional[Union[str, None]] = None
    gravatarHash: Optional[str] = None
    joined: Optional[datetime] = None
    lastSeen: Optional[datetime] = None
    plansCount: Optional[int] = 0
    plansDistance: Optional[float] = 0.0
    plansDownloads: Optional[int] = 0
    plansLikes: Optional[int] = 0

    def __post_init__(self):
        self.joined = isoparse(self.joined) \
            if self.joined else self.joined
        self.lastSeen = isoparse(self.lastSeen) \
            if self.lastSeen else self.lastSeen


@dataclass
class UserSmall:
    """Describes users registered on the website, with far less info

    Attributes
    ----------
    id : int
        Unique user identifier number
    username : str
        Username
    location : Optional[Union[str, None]]
        User provided location information. ``None`` if not available
    gravatarHash : Optional[str]
        Gravatar hash based on user's account email address.
    """
    id: int
    username: str
    location: Optional[Union[str, None]] = None
    gravatarHash: Optional[str] = None


@dataclass
class Application:
    """Describes application associated with a flight plan

    Attributes
    ----------
    id : int
        Unique application identifier number
    name : Optional[Union[str, None]]
        Application name
    url : Optional[Union[str, None]]
        Application URL
    """
    id: int
    name: Optional[Union[str, None]] = None
    url: Optional[Union[str, None]] = None


@dataclass
class Via:
    """Describes routes to :class:`RouteNode` s

    Attributes
    ----------
    ident : str
        desc
    type : str
        Type of Via; must be one of :py:obj:`Via.validtypes`
    validtypes : List[str]
        Do not change. Valid Via types.
    """
    ident: str
    type: str

    validtypes = ['SID', 'STAR', 'AWY-HI', 'AWY-LO', 'NAT', 'PACOT']

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid Via type")


@dataclass
class RouteNode:
    """Describes nodes in :class:`Route` s

    Attributes
    ----------
    ident : str
        Node navaid identifier
    type : str
        Type of RouteNode; must be one of :py:obj:`RouteNode.validtypes`
    lat : float
        Node latitude in decimal degrees
    lon : float
        Node longitude in decimal degrees
    alt : float
        Suggested altitude at node
    name : Union[str, None]
        Node name.
    via : Union[Via, None]
        Route to node.
    validtypes : List[str]
        Do not change. Valid RouteNode types.
    """
    ident: str
    type: str
    lat: float
    lon: float
    alt: float
    name: Union[str, None]
    via: Union[Via, None]

    validtypes = ['UKN', 'APT', 'NDB', 'VOR', 'FIX', 'DME', 'LATLON']

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid RouteNode type")
        self.via = Via(**self.via) if type(self.via) == dict else self.via


@dataclass
class Route:
    """Describes the route of a :class:`Plan`

    Attributes
    ----------
    nodes : List[RouteNode]
        A list of :class:`RouteNode` s. A route must have at least 2 nodes.
    """
    nodes: List[RouteNode]

    def __post_init__(self):
        self.nodes = list(
            map(
                lambda x: RouteNode(**x) if type(x) == dict else x,
                self.nodes
                )
            )


@dataclass
class Cycle:
    """Navdata cycle

    Attributes
    ----------
    id : int
        FlightPlanDB cycle id
    ident : str
        AIP-style cycle id
    year : int
        Last two digits of cycle year
    release : int
        Cycle release
    """
    id: int
    ident: str
    year: int
    release: int


@dataclass
class Plan:
    """A flight plan; the thing this whole API revolves around

    Attributes
    ----------
    id : int
        Unique plan identifier number
    fromICAO : Union[str, None]
        ICAO code of the departure airport
    toICAO : Union[str, None]
        ICAO code of the destination airport
    fromName : Union[str, None]
        Name of the departure airport
    toName : Union[str, None]
        Name of the destination airport
    flightNumber : Optional[Union[str, None]]
        Flight number of the flight plan
    distance : Optional[float]
        Total distance of the flight plan route
    maxAltitude : Optional[float]
        Maximum altitude of the flight plan route
    waypoints : Optional[int]
        Number of nodes in the flight plan route
    likes : Optional[int]
        Number of times the flight plan has been liked
    downloads : Optional[int]
        Number of times the flight plan has been downloaded
    popularity : Optional[int]
        Relative popularity of the plan based on downloads and likes
    notes : Optional[str]
        Extra information about the flight plan
    encodedPolyline : Optional[str]
        Encoded polyline of route, which can be used for quickly drawing maps
    createdAt : Optional[datetime]
        UTC Date and time of flight plan creation
    updatedAt : Optional[datetime]
        UTC Date and time of the last flight plan edit
    tags : Optional[List[str]]
        List of flight plan tags
    user : Optional[Union[User, None]]
        User associated with the item. ``None`` if no user linked
    application : Optional[Union[Application, None]]
        Application associated with the item. ``None`` if no application linked
    route : Optional[Route]
        The flight plan route
    cycle : Optional[Cycle]
        The navigation data cycle
    """
    id: int
    fromICAO: Union[str, None]
    toICAO: Union[str, None]
    fromName: Union[str, None]
    toName: Union[str, None]
    flightNumber: Optional[Union[str, None]] = None
    distance: Optional[float] = None
    maxAltitude: Optional[float] = None
    waypoints: Optional[int] = None
    likes: Optional[int] = None
    downloads: Optional[int] = None
    popularity: Optional[int] = None
    notes: Optional[str] = None
    encodedPolyline: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    tags: Optional[List[str]] = None
    user: Optional[Union[User, None]] = None
    application: Optional[Union[Application, None]] = None
    route: Optional[Route] = None
    cycle: Optional[Cycle] = None

    def __post_init__(self):
        self.createdAt = (isoparse(self.createdAt)
                          if type(self.createdAt) != datetime
                          else self.createdAt)
        self.updatedAt = (isoparse(self.updatedAt)
                          if type(self.updatedAt) != datetime
                          else self.updatedAt)

        self.user = User(**self.user) if self.user else self.user
        if self.application:
            self.application = Application(**self.application)
        self.route = (Route(self.route)
                      if type(self.route) == list else self.route)
        self.cycle = (Cycle(**self.cycle)
                      if type(self.cycle) == dict else self.cycle)


@dataclass
class PlanQuery:
    """Simple search query.

    Attributes
    ----------
    q : Optional[str]
        Username, tags and the flight number
    From : Optional[str]
        From search query. Search departure ICAO & name
    to : Optional[str]
        To search query. Search departure ICAO & name
    fromICAO : Optional[str]
        Matches departure airport ICAO
    toICAO : Optional[str]
        Matches destination airport ICAO
    fromName : Optional[str]
        Matches departure airport name
    toName : Optional[str]
        Matches destination airport name
    flightNumber : Optional[str]
        Matches flight number
    distanceMin : Optional[str]
        Minimum route distance
    distanceMax : Optional[str]
        Maximum route distance, with units determined by the X-Units header
    tags : Optional[str]
        Tag names to search, comma separated
    includeRoute : Optional[str]
        Include route objects for each plan in the response.
        Setting to true requires the request be authenticated with an API key
    sort : Optional[str]
        The order of the returned plans. See Pagination for more options
    """
    q: Optional[str] = None
    From: Optional[str] = None
    to: Optional[str] = None
    fromICAO: Optional[str] = None
    toICAO: Optional[str] = None
    fromName: Optional[str] = None
    toName: Optional[str] = None
    flightNumber: Optional[str] = None
    distanceMin: Optional[str] = None
    distanceMax: Optional[str] = None
    tags: Optional[str] = None
    includeRoute: Optional[str] = None
    limit: Optional[int] = None
    sort: Optional[str] = None

    def as_dict(self):
        return {
            f.name[0].lower()+f.name[1:]: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name)
        }


@dataclass
class GenerateQuery:
    """Generate plan query.

    Attributes
    ----------
    fromICAO : str
        The departure airport ICAO code
    toICAO : str
        The destination airport ICAO code
    useNAT : Optional[bool]
        Use Pacific Organized Track System tracks in the route generation
    usePACOT : Optional[bool]
        Use Pacific Organized Track System tracks in the route generation
    useAWYLO : Optional[bool]
        Use low-level airways in the route generation
    useAWYHI : Optional[bool]
        Use high-level airways in the route generation
    cruiseAlt : Optional[float]
        Basic flight profile cruise altitude (altitude)
    cruiseSpeed : Optional[float]
        Basic flight profile cruise speed (speed)
    ascentRate : Optional[float]
        Basic flight profile ascent rate (climb rate)
    ascentSpeed : Optional[float]
        Basic flight profile ascent speed (speed)
    descentRate : Optional[float]
        Basic flight profile descent rate (climb rate)
    descentSpeed : Optional[float]
        Basic flight profile descent speed (speed)
    """
    fromICAO: str
    toICAO: str
    useNAT: Optional[bool] = True
    usePACOT: Optional[bool] = True
    useAWYLO: Optional[bool] = True
    useAWYHI: Optional[bool] = True
    cruiseAlt: Optional[float] = 35000
    cruiseSpeed: Optional[float] = 420
    ascentRate: Optional[float] = 2500
    ascentSpeed: Optional[float] = 250
    descentRate: Optional[float] = 1500
    descentSpeed: Optional[float] = 250


@dataclass
class Tag:
    """Flight plan tag

    Attributes
    ----------
    name : str
        Tag name
    description : Union[str, None]
        Description of the tag. ``None`` if no description is available
    planCount : int
        Number of plans with this tag
    popularity: int
        Popularity index of the tag
    """
    name: str
    description: Union[str, None]
    planCount: int
    popularity: int


@dataclass
class Timezone:
    """Contains timezone information

    Attributes
    ----------
    name : Union[str, None]
        The IANA timezone the airport is located in. ``None`` if not available
    offset : Union[float, None]
        The number of seconds the airport timezone is currently offset from UTC.
        Positive is ahead of UTC. ``None`` if not available
    """
    name: Union[str, None]
    offset: Union[float, None]


@dataclass
class Times:
    """Contains relevant times information

    Attributes
    ----------
    sunrise : datetime
        Time of sunrise
    sunset : datetime
        Time of sunset
    dawn : datetime
        Time of dawn
    dusk : datetime
        Time of dusk
    """
    sunrise: datetime
    sunset: datetime
    dawn: datetime
    dusk: datetime

    def __post_init__(self):
        self.sunrise = (isoparse(self.sunrise)
                        if type(self.sunrise) != datetime
                        else self.sunrise)
        self.sunset = (isoparse(self.sunset)
                       if type(self.sunset) != datetime
                       else self.sunset)
        self.dawn = (isoparse(self.dawn)
                     if type(self.dawn) != datetime
                     else self.dawn)
        self.dusk = (isoparse(self.dusk)
                     if type(self.dusk) != datetime
                     else self.dusk)


@dataclass
class RunwayEnds:
    """Ends of :class:`Runway` . No duh.

    Attributes
    ----------
    ident : str
        The identifier of the runway end
    lat : float
        The latitude of the runway end
    lon : float
        The longitude of the runway end
    """
    ident: str
    lat: float
    lon: float


@dataclass
class Navaid:
    """Describes a navigational aid

    Attributes
    ----------
    ident: str
        The navaid identifier
    type: str
        The navaid type. Must be one of :py:obj:`Navaid.validtypes`
    lat: float
        The navaid latitude
    lon: float
        The navaid longitude
    airport: str
        The airport associated with the navaid
    runway: str
        The runway associated with the navaid
    frequency: Union[float, None]
        The navaid frequency in Hz. ``None`` if not available
    slope: Union[float, None]
        The navaid slope in degrees from horizontal used for type GS
    bearing: Union[float, None]
        The navaid bearing in true degrees. ``None`` if not available
    name: Union[float, None]
        The navaid name. ``None`` if not available
    elevation: float
        The navaid elevation above mean sea level (elevation)
    range: float
        The navaid range, with units determined by the X-Units header (distance)
    validtypes : List[str]
        Do not change. Valid Navaid types.
    """
    ident: str
    type: str
    lat: float
    lon: float
    airport: str
    runway: str
    frequency: Union[float, None]
    slope: Union[float, None]
    bearing: Union[float, None]
    name: Union[float, None]
    elevation: float
    range: float

    validtypes = ['LOC-ILS', 'LOC-LOC', 'GS', 'DME']

    def __post_init__(self):
        if self.type not in self.validtypes:
            raise ValueError(f"{self.type} is not a valid Navaid type")


@dataclass
class Runway:
    """Describes a runway at an :class:`Airport`

    Attributes
    ----------
    ident: str
        The runway identifier
    width: float
        The runway width, with units determined by the X-Units header (length)
    length: float
        The runway length, with units determined by the X-Units header (length)
    bearing: float
        The runway bearing in true degrees
    surface: str
        The runway surface material
    markings: List[str]
        List of strings of runway markings
    lighting: List[str]
        List of strings of runway lighting types
    thresholdOffset: float
        The distance of the displaced threshold from the runway end (length)
    overrunLength: float
        The runway overrun length, with units determined by the X-Units header
    ends: List[RunwayEnds]
        Two element List containing the location of the two ends of the runway
    navaids: List[Navaid]
        List of navaids associated with the current runway
    """
    ident: str
    width: float
    length: float
    bearing: float
    surface: str
    markings: List[str]
    lighting: List[str]
    thresholdOffset: float
    overrunLength: float
    ends: List[RunwayEnds]
    navaids: List[Navaid]

    def __post_init__(self):
        self.ends = list(map(lambda rw: RunwayEnds(**rw), self.ends))
        self.navaids = list(map(lambda n: Navaid(**n), self.navaids))


@dataclass
class Frequency:
    """Holds frequency information

    Attributes
    ----------
    type : str
        The frequency type
    frequency : float
        The frequency in Hz
    name : Union[str, None]
        The frequency name. ``None`` if not available

    """
    type: str
    frequency: float
    name: Union[str, None]


@dataclass
class Weather:
    """Contains weather reports and predictions

    Attributes
    ----------
    METAR : Union[str, None]
        Current METAR report for the airport
    TAF : Union[str, None]
        Current TAF report for the airport
    """
    METAR: Union[str, None]
    TAF: Union[str, None]


@dataclass
class Airport:
    """Describes an airport

    Attributes
    ----------
    ICAO: str
        The airport ICAO code
    IATA: Union[str, None]
        The airport IATA code. ``None`` if not available
    name: str
        The airport name
    regionName: Union[str, None]
        The geographical region the airport is located in.
        ``None`` if not available
    elevation: float
        The airport elevation above mean sea level (elevation)
    lat: float
        The airport latitude in degrees
    lon: float
        The airport longitude in degrees
    magneticVariation: float
        The current magnetic variation/declination at the airport,
        based on the World Magnetic Model
    timezone: Timezone
        The airport timezone information
    times: Times
        Relevant times at the airport
    runwayCount: int
        The number of runways at the airport
    runways: List[Runway]
        List of runways.
        Note: each physical runway will appear twice, once from each end
    frequencies: List[Frequency]
        List of frequencies associated with the airport
    weather: Weather
        Airport weather information
    """
    ICAO: str
    IATA: Union[str, None]
    name: str
    regionName: Union[str, None]
    elevation: float
    lat: float
    lon: float
    magneticVariation: float
    timezone: Timezone
    times: Times
    runwayCount: int
    runways: List[Runway]
    frequencies: List[Frequency]
    weather: Weather

    def __post_init__(self):
        self.timezone = Timezone(**self.timezone)
        self.runways = list(map(lambda rw: Runway(**rw), self.runways))
        self.frequencies = list(
            map(lambda rw: Frequency(**rw), self.frequencies))
        self.weather = Weather(**self.weather)


@dataclass
class Track:
    """Used for NATS and PACOTS tracks

    Attributes
    ----------
    ident : str
        Track identifier
    route : Route
        Route of the track
    validFrom : datetime
        UTC datetime the track is valid from
    validTo : datetime
        UTC datetime the track is valid to
    """
    ident: str
    route: Route
    validFrom: datetime
    validTo: datetime

    def __post_init__(self):
        self.validFrom = isoparse(self.validFrom)
        self.validTo = isoparse(self.validTo)