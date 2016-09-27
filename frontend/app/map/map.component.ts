import { Component, ViewChild, AfterViewInit, NgZone } from "@angular/core";
import { trigger, state, style, transition, animate } from "@angular/core"; // animation import

import { MapObject, MapObjectType, MapService } from "./";

export enum DateFilter {
    all = 0,
    upcoming,
    year2016,
    year2015,
}

class MapFilter {
    constructor(
        public name: string, public infoText: string, public filter: DateFilter,
        public iconPath: string, public iconClickedPath: string, public opacityBasedOnDate: boolean,
    ) {}
}

class MapObjectSetting {
        constructor(
            public visible: boolean = false, public name: string,
            public mapFilter: MapFilter, public mapFilterOptions: MapFilter[],
        ) {}
}

@Component({
    moduleId: module.id,
    selector: "cg-map",
    templateUrl: "map.component.html",
    providers: [MapService],
    animations: [
        trigger("slideInOut", [
            state("in", style({height: "*"})),
            transition("* => void", [
                animate("250ms ease-out", style({height: 0})),
            ]),
            transition("void => *", [
                style({height: 0}),
                animate("250ms ease-out", style({height: "*"})),
            ]),
        ]),
    ],
})
export class MapComponent implements AfterViewInit {

    private errorMessage: string;
    private errorMessageDisplayTime: number = 5000;
    private map: google.maps.Map;
    // Utilized for holding status and name of different types of MapObjects
    private mapObjectSettings: Array<MapObjectSetting> = new Array<MapObjectSetting>();
    // Value list of different MapObject types to decrease redundant code
    private mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
    private markers: Map<MapObjectType, Array<google.maps.Marker>> =
        new Map<MapObjectType, Array<google.maps.Marker>>();

    private selectedMapObject: MapObject;
    private selectedMapObjectType: MapObjectType;
    private selectedMarker: google.maps.Marker;

    @ViewChild("mapCanvas") private mapCanvas;

    constructor(private mapService: MapService, private zone: NgZone) {
        this.initializeMarkerMap();
        this.initializeMapObjectSettings();
    }

    public ngAfterViewInit() {
        this.initMap();
        this.retrieveVisibleMapObjects();
    }

    public onCheckboxChange() {
        this.retrieveVisibleMapObjects();
        this.deleteNotVisibleMapObjects();
    }

    public onRadioChange() {
        for (let marker of this.markers.get(MapObjectType.EVENTS)) {
            marker.setMap(null);
        }
        this.markers.set(MapObjectType.EVENTS, new Array<google.maps.Marker>());
        this.retrieveVisibleMapObjects();
    }

    private initMap() {
        const latlng = new google.maps.LatLng(51.0679567, 13.5767141);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 10,
            zoomControl: true,
            mapTypeControl: false,
            streetViewControl: false,
        };
        this.map = new google.maps.Map(this.mapCanvas.nativeElement, mapOptions);
        this.map.addListener("click", () =>  this.updateSelectedMapObjectInfo(null, null, null));
    }

    private retrieveVisibleMapObjects() {
        this.updateSelectedMapObjectInfo(null, null, null);
        for (let mapObjectType of this.mapObjectTypes) {
            if (this.mapObjectSettings[mapObjectType].visible) {
                this.mapService.getMapObjects(mapObjectType, this.mapObjectSettings[mapObjectType].mapFilter.filter)
                            .subscribe(
                                mapObjects => this.drawMapObjects(mapObjects, mapObjectType),
                                error => this.setErrorMessage(<any> error)
                            );
            }
        }
    }

    private drawMapObjects(mapObjects: MapObject[], mapObjectType: MapObjectType) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject, mapObjectType));
    }

    private calcMapObjectOpacity(mapObject: MapObject, mapObjectType: MapObjectType) {
        // If MapObject does not have a date (is a facebook page at the current project state)
        if (!this.mapObjectSettings[mapObjectType].mapFilter.opacityBasedOnDate) {
            return 1.0;
        }

        const today = new Date();
        if (today <= new Date(mapObject.date)) {
            return 1.0;
        } else {
            return 0.2;
        }
    }

    private drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name,
            icon: this.mapObjectSettings[mapObjectType].mapFilter.iconPath,
            opacity: this.calcMapObjectOpacity(mapObject, mapObjectType),
        });

        marker.addListener("click", (() => {
            this.updateSelectedMapObjectInfo(mapObject, mapObjectType, marker);
            if (this.willInfoBoxHideMarker(marker)) {
                this.map.panTo(marker.getPosition());
            }
        }));
        marker.setMap(this.map);
        this.markers.get(mapObjectType).push(marker);
    }

    private initializeMapObjectSettings() {
        let mapEventFilterOptions = [
            new MapFilter(
                "aktuell", "kommende & vergangene Veranst. (30 Tage)",
                DateFilter.upcoming, "static/img/schild_magenta.png", "static/img/schild_aktiv_magenta.png", true,
            ),
            new MapFilter(
                "2016", null, DateFilter.year2016,
                "static/img/schild_schwarz.png", "static/img/schild_aktiv_schwarz.png", false,
            ),
            new MapFilter(
                "2015", null, DateFilter.year2015,
                "static/img/schild_schwarz.png", "static/img/schild_aktiv_schwarz.png", false
            ),
        ];
        this.mapObjectSettings[MapObjectType.EVENTS] =
            new MapObjectSetting(true, "Veranstaltungen", mapEventFilterOptions[0], mapEventFilterOptions);

        let mapFacebookPagesFilterOptions = new MapFilter(
            "alle", null, DateFilter.all,
            "static/img/facebook.png", "static/img/facebook_aktiv.png", false
        );
        this.mapObjectSettings[MapObjectType.FACEBOOK_PAGES] =
            new MapObjectSetting(false, "Facebook-Seiten", mapFacebookPagesFilterOptions, []);
    }

    private initializeMarkerMap() {
        for (let mapObjectType of this.mapObjectTypes) {
            this.markers.set(mapObjectType, new Array<google.maps.Marker>());
        }
    }

    private deleteNotVisibleMapObjects() {
        for (let mapObjectType of this.mapObjectTypes) {
            if (!this.mapObjectSettings[mapObjectType].visible && this.markers.get(mapObjectType).length > 0) {
                for (let marker of this.markers.get(mapObjectType)) {
                    marker.setMap(null);
                }
                this.markers.set(mapObjectType, new Array<google.maps.Marker>());
            }
        }
    }

    private updateSelectedMapObjectInfo(mapObject: MapObject, mapObjectType: MapObjectType,
                                        marker: google.maps.Marker) {
        this.zone.run(() => {
            if (this.selectedMarker) {
                this.selectedMarker.setIcon(this.mapObjectSettings
                    [this.selectedMapObjectType].mapFilter.iconPath);
            }

            if (marker) {
                marker.setIcon(this.mapObjectSettings[mapObjectType].mapFilter.iconClickedPath);
            }

            this.selectedMapObject = mapObject;
            this.selectedMapObjectType = mapObjectType;
            this.selectedMarker = marker;
        });
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
        const tmpScope = this;
        setTimeout(function(){
            tmpScope.errorMessage = "";
        }, this.errorMessageDisplayTime);
    }

    private willInfoBoxHideMarker(marker: google.maps.Marker) {
        const infoBoxWidth = 320; // incl. padding
        const windowWidth = this.mapCanvas.nativeElement.clientWidth;

        const longitudeWest = this.map.getBounds().getSouthWest().lng();
        const longitudeEast = this.map.getBounds().getNorthEast().lng();
        const mapWidth = longitudeEast - longitudeWest;
        const markerLngRelative = marker.getPosition().lng() - longitudeWest;

        // We compare the ratio of the width of info box and window with the ratio of the longitude
        // of the marker (realtive to the left border of the map) and the range of shown longitude of the map.
        return (infoBoxWidth / windowWidth) > (markerLngRelative / mapWidth);
    }
}
