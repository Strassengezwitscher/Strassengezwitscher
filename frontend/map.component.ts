import { Component, ViewChild, AfterViewInit, NgZone } from "@angular/core";

import { MapObject, MapObjectType } from "./mapObject";
import { MapService } from "./map.service";

export class MapObjectSetting {
        constructor(public active: boolean = false, public iconPath: string, public name: string) {}
}

@Component({
    moduleId: module.id,
    selector: "cg-map",
    templateUrl: "map.component.html",
    providers: [MapService],
})

export class MapComponent implements AfterViewInit {

    private errorMessage: string;
    private map: google.maps.Map;
    // Utilized for holding status and name of different types of MapObjects
    private mapObjectSettings: Array<MapObjectSetting> = new Array<MapObjectSetting>();
    // Value list of different MapObject types to decrease redundant code
    private mapObjectTypes = Object.keys(MapObjectType).map(k => MapObjectType[k]).filter(v => typeof v === "number");
    private markers: Map<MapObjectType, Array<google.maps.Marker>> =
        new Map<MapObjectType, Array<google.maps.Marker>>();
    private mapSideInfoState: string;
    private currentlyActiveMapObject: MapObject = new MapObject();

    @ViewChild("mapCanvas") private mapCanvas;
    @ViewChild("sidenav") private sidenav;

    constructor(private mapService: MapService,  private zone: NgZone) {
        this.initializeMarkerMap();
        this.initializeMapObjectSettings();
        this.mapSideInfoState = "info";
    }

    public ngAfterViewInit() {
        this.initMap();
        this.retrieveVisibleMapObjects();
    }

    public onCheckboxChange() {
        this.retrieveVisibleMapObjects();
        this.deleteNotVisibleMapObjects();
    }

    private initMap() {
        const latlng = new google.maps.LatLng(51.0679567, 13.5767141);
        const mapOptions = {
            center: latlng,
            scrollWheel: false,
            zoom: 10,
        };
        this.map = new google.maps.Map(this.mapCanvas.nativeElement, mapOptions);
    }

    private retrieveVisibleMapObjects() {
        for (let mapObjectType of this.mapObjectTypes) {
            if (this.mapObjectSettings[mapObjectType].active) {
                this.mapService.getMapObjects(mapObjectType)
                            .subscribe(
                                mapObjects => this.drawMapObjects(mapObjects, mapObjectType),
                                error => this.errorMessage = <any> error
                            );
            }
        }
    }

    private drawMapObjects(mapObjects: MapObject[], mapObjectType: MapObjectType) {
        mapObjects.map((mapObject) => this.drawMapObject(mapObject, mapObjectType));
    }

    private drawMapObject(mapObject: MapObject, mapObjectType: MapObjectType) {
        const latLng = new google.maps.LatLng(mapObject.locationLat, mapObject.locationLong);
        const marker = new google.maps.Marker({
            position: latLng,
            title: mapObject.name,
            icon: this.mapObjectSettings[mapObjectType].iconPath,
        });

        marker.addListener("click", (() => {
            this.openSideNav();
            this.updateCurrentlyActiveMapObject(mapObject);
        }));
        marker.setMap(this.map);
        this.markers.get(mapObjectType).push(marker);
    }

    private initializeMapObjectSettings() {
        this.mapObjectSettings[MapObjectType.EVENTS] =
            new MapObjectSetting(true, "static/img/schild_schwarz.png", "Veranstaltungen");
        this.mapObjectSettings[MapObjectType.FACEBOOK_PAGES] =
            new MapObjectSetting(false, "static/img/schild_blau.png", "Facebook-Seiten");
    }

    private initializeMarkerMap() {
        for (let mapObjectType of this.mapObjectTypes) {
            this.markers.set(mapObjectType, new Array<google.maps.Marker>());
        }
    }

    private deleteNotVisibleMapObjects() {
        for (let mapObjectType of this.mapObjectTypes) {
            if (!this.mapObjectSettings[mapObjectType].active && this.markers.get(mapObjectType).length > 0) {
                for (let marker of this.markers.get(mapObjectType)) {
                    marker.setMap(null);
                }
                this.markers.set(mapObjectType, new Array<google.maps.Marker>());
            }
        }
    }

    private updateCurrentlyActiveMapObject(mapObject: MapObject) {
        this.zone.run(() => {
            this.currentlyActiveMapObject = mapObject;
        });
    }

    private openSideNav() {
        if (!this.sidenav._isOpened) {
            this.sidenav.toggle();
        }
    }
}
