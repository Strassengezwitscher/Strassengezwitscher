import { Component, ViewChild, AfterViewInit, NgZone } from "@angular/core";
import { trigger, state, style, transition, animate } from "@angular/core"; // animation import

import { Helper } from "../helper";
import { MapObject, MapObjectType } from "./mapObject.model";
import { MapService } from "./map.service";

export enum DateFilter {
    all = 0,
    upcoming,
    year2016,
    year2015,
}

class MapFilter {
    constructor(
        public name: string, public infoText: string, public filter: DateFilter,
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
    styleUrls: ["map.component.css"],
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
    public errorMessage: string;
    // Utilized for holding status and name of different types of MapObjects
    public mapObjectSettings: Array<MapObjectSetting> = new Array<MapObjectSetting>();
    public selectedMapObjectType: MapObjectType;
    @ViewChild("mapCanvas") public mapCanvas;
    private errorMessageDisplayTime: number = 5000;
    private map: google.maps.Map;
    // Value list of different MapObject types to decrease redundant code
    private mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
    private markers: Map<MapObjectType, Array<google.maps.Marker>> =
        new Map<MapObjectType, Array<google.maps.Marker>>();
    private selectedMapObject: MapObject;
    private selectedMarker: google.maps.Marker;

    constructor(private mapService: MapService, private zone: NgZone) {
        this.initializeMarkerMap();
        this.initializeMapObjectSettings();
    }

    public ngAfterViewInit() {
        this.initMap();
    }

    public onCheckboxChange(mapObjectSetting: MapObjectSetting) {
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

    public clearInfoBox() {
        this.updateSelectedMapObjectInfo(null, null, null);
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
            // Retrieve MapObjects only if currently visible and markers do not yet exist
            if (this.mapObjectSettings[mapObjectType].visible && this.markers.get(mapObjectType).length < 1) {
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

    // TODO: should be part of the mapObject refactoring
    // cannot currently not be in mapObject.model.ts because mapObject is not really of type MapObject
    private setIconsAndOpacity(mapObject: MapObject, iconPath: string, iconSelectedPath: string, opacity: number) {
        mapObject.iconPath = iconPath;
        mapObject.iconSelectedPath = iconSelectedPath;
        mapObject.opacity = opacity;
    }

    // TODO: should be part of the mapObject refactoring
    private determineMapObjectAppearance(mapObject: MapObject, mapObjectType: MapObjectType) {
        if (mapObjectType === MapObjectType.FACEBOOK_PAGES) {
            this.setIconsAndOpacity(mapObject, "static/img/facebook.png",
                                        "static/img/facebook_aktiv.png", 1.0);
        } else {
            if (this.mapObjectSettings[mapObjectType].mapFilter.name === "2015" ||
                this.mapObjectSettings[mapObjectType].mapFilter.name === "2016") {
                this.setIconsAndOpacity(mapObject, "static/img/schild_schwarz.png",
                                        "static/img/schild_aktiv_schwarz.png", 1.0);
            } else if (this.mapObjectSettings[mapObjectType].mapFilter.name === "aktuell") {
                const today = new Date();
                if (Helper.nextDay(mapObject.date) >= today) {
                    this.setIconsAndOpacity(mapObject, "static/img/schild_magenta.png",
                                        "static/img/schild_aktiv_magenta.png", 1.0);
                } else {
                    this.setIconsAndOpacity(mapObject, "static/img/schild_schwarz.png",
                                        "static/img/schild_aktiv_schwarz.png", 0.3);
                }
            }
        }
    }

    private drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        this.determineMapObjectAppearance(mapObject, mapObjectType);
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name,
            icon: mapObject.iconPath,
            opacity: mapObject.opacity,
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
                "aktuell", "Kommende & vergangene Veranstaltungen (30 Tage)", DateFilter.upcoming,
            ),
            new MapFilter(
                "2016", null, DateFilter.year2016,
            ),
            new MapFilter(
                "2015", "Mit freundlicher Genehmigung von rechtes-sachsen.de", DateFilter.year2015,
            ),
        ];
        this.mapObjectSettings[MapObjectType.EVENTS] =
            new MapObjectSetting(true, "Veranstaltungen", mapEventFilterOptions[0],
                                mapEventFilterOptions);

        let mapFacebookPagesFilterOptions = [
            new MapFilter(
                "alle", null, DateFilter.all,
            ),
        ];
        this.mapObjectSettings[MapObjectType.FACEBOOK_PAGES] =
            new MapObjectSetting(false, "Facebook-Seiten", mapFacebookPagesFilterOptions[0],
                                mapFacebookPagesFilterOptions);
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
                this.selectedMarker.setIcon(this.selectedMapObject.iconPath);
            }

            if (marker) {
                marker.setIcon(mapObject.iconSelectedPath);
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
