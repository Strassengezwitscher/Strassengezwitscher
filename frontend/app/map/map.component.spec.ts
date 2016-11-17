import { BaseRequestOptions, Http } from "@angular/http";
import { MockBackend } from "@angular/http/testing";
import { NgZone } from "@angular/core";

import { MapObjectType } from "./mapObject.model";
import { MapComponent } from "./map.component";
import { MapService } from "./map.service";

describe("MapComponent", () => {

    beforeEach(() => {
        this.mapComponent = new MapComponent(new MapService(new Http(new MockBackend(), new BaseRequestOptions())),
                                             new NgZone(true));
    });

    it("Should have an initialized markerMap and mapObjectSettings after construction", done => {
        expect(this.mapComponent.markers.size).toBe(this.mapComponent.mapObjectTypes.length);
        for (let mapObjectType of this.mapComponent.mapObjectTypes) {
            expect(this.mapComponent.markers.get(mapObjectType).length).toBe(0);
            expect(this.mapComponent.markers.get(mapObjectType) instanceof Array).toBeTruthy();
        }

        expect(this.mapComponent.mapObjectSettings.length).toBe(this.mapComponent.mapObjectTypes.length);

        done();
    });

    it("Should retrieve visible objects and delete not visible ones onCheckboxChange", done => {
        spyOn(this.mapComponent, "deleteNotVisibleMapObjects");
        spyOn(this.mapComponent, "retrieveVisibleMapObjects");

        // The point is that deleteNotVisibleMapObjects gets called each time when onCheckboxChange is triggered,
        // but retrieveVisibleMapObjects will only be called if there is only one filter option (FACEBOOK_PAGES)

        this.mapComponent.onCheckboxChange(this.mapComponent.mapObjectSettings[MapObjectType.FACEBOOK_PAGES]);
        expect(this.mapComponent.deleteNotVisibleMapObjects).toHaveBeenCalledTimes(1);
        expect(this.mapComponent.retrieveVisibleMapObjects).toHaveBeenCalledTimes(1);

        this.mapComponent.onCheckboxChange(this.mapComponent.mapObjectSettings[MapObjectType.EVENTS]);
        expect(this.mapComponent.deleteNotVisibleMapObjects).toHaveBeenCalledTimes(2);
        expect(this.mapComponent.retrieveVisibleMapObjects).toHaveBeenCalledTimes(2);

        done();
    });

});
