import { TestBed, inject } from "@angular/core/testing";
import { BaseRequestOptions, Http, Response, ResponseOptions } from "@angular/http";
import { MockBackend } from "@angular/http/testing";

import { DateFilter } from "./map.component";
import { MapObjectType } from "./mapObject.model";
import { MapService } from "./map.service";

describe("MapService", () => {
    beforeEach(() => {
        // Set mockdate to 31st of May 2017
        let mockDate = new Date(2017, 4, 31);
        jasmine.clock().mockDate(mockDate);

        TestBed.configureTestingModule({
            providers: [
                MapService,
                MockBackend,
                BaseRequestOptions,
                {
                    provide: Http,
                    useFactory: (backend, options) => new Http(backend, options),
                    deps: [MockBackend, BaseRequestOptions],
                },
            ],
        });
    });

    it("Should return mocked response", inject([MockBackend, MapService], (mockBackend, service) => {
        let response = [
            {
                "id": 13,
                "name": "Wurstverein Boltenhagen",
                "active": true,
                "location": "Berlin",
                "locationLong": "13.738144",
                "locationLat": "51.049329",
            },
            {
                "id": 25,
                "name": "BVB",
                "active": false,
                "location": "Frankfurt",
                "locationLong": "13.738144",
                "locationLat": "51.049329",
            },
        ];

        mockBackend.connections.subscribe(connection => {
            connection.mockRespond(new Response(new ResponseOptions({body: JSON.stringify(response)})));
        });
        service.getMapObjects(MapObjectType.EVENTS, DateFilter.all).subscribe(mapObjects => {
            expect(mapObjects).toContain({
                "id": 13,
                "name": "Wurstverein Boltenhagen",
                "active": true,
                "location": "Berlin",
                "locationLong": "13.738144",
                "locationLat": "51.049329",
            });
            expect(mapObjects).toContain({
                "id": 25,
                "name": "BVB",
                "active": false,
                "location": "Frankfurt",
                "locationLong": "13.738144",
                "locationLat": "51.049329",
            });
            expect(mapObjects.length).toBe(2);
        });
    }));

    it("Should return empty array if server answer is empty",
       inject([MockBackend, MapService], (mockBackend, service) => {
        let emptyResponse = [];
        mockBackend.connections.subscribe(connection => {
            connection.mockRespond(new Response(new ResponseOptions({body: JSON.stringify(emptyResponse)})));
        });
        service.getMapObjects(MapObjectType.EVENTS, DateFilter.all).subscribe(mapObjects => {
            expect(mapObjects.length).toBe(0);
        });
    }));

    it("Should return JSON Parse error if server responds malforemd",
       inject([MockBackend, MapService], (mockBackend, service) => {
        let malformedResponse = "[{\"id\": 25, \"name\":}]";

        mockBackend.connections.subscribe(connection => {
            connection.mockRespond(new Response(new ResponseOptions({body: malformedResponse, status: 500})));
        });
        try {
            service.getMapObjects(MapObjectType.EVENTS, DateFilter.all).subscribe();
        } catch (error) {
            expect(error).toBe("JSON Parse error: Unexpected token '}'");
        }
    }));

    it("Should return server error if Internal Server Error occurs",
       inject([MockBackend, MapService], (mockBackend, service) => {
        mockBackend.connections.subscribe(connection => {
            connection.mockError(new Error("Internal Server Error 500"));
        });
        try {
            service.getMapObjects(MapObjectType.EVENTS, DateFilter.all).subscribe();
        } catch (error) {
            expect(error).toBe("Internal Server Error 500");
        }
    }));

    it("Should return error status code and text if present", inject([MapService], (service) => {
        spyOn(service, "handleError").and.callThrough();
        let err = {statusText: "Resource not found", status: 404};

        expect(service.handleError(err).error).toBe("404 - Resource not found");
    }));

    it("Should have an initialized urlMap after construction", inject([MapService], (service) => {
        expect(service.urlMap.size).toBe(2);
        expect(service.urlMap.get(MapObjectType.EVENTS).size).toBe(5);
        expect(service.urlMap.get(MapObjectType.FACEBOOK_PAGES).size).toBe(1);
        expect(service.urlMap.get(MapObjectType.EVENTS).get(DateFilter.all)).toBe("api/events.json");
        expect(service.urlMap.get(MapObjectType.FACEBOOK_PAGES).get(DateFilter.all)).toBe("api/facebook.json");

        expect(service.urlMap.get(MapObjectType.EVENTS).get(DateFilter.year2015)).
            toBe("api/events.json?from=2015-01-01&to=2015-12-31");
        expect(service.urlMap.get(MapObjectType.EVENTS).get(DateFilter.year2016)).
            toBe("api/events.json?from=2016-01-01&to=2016-12-31");
        expect(service.urlMap.get(MapObjectType.EVENTS).get(DateFilter.year2017)).
            toContain("api/events.json?from=2017-01-01&");

        // Folling two specs based on mocked date
        expect(service.urlMap.get(MapObjectType.EVENTS).get(DateFilter.year2017)).
            toContain("to=2017-5-31");
        expect(service.urlMap.get(MapObjectType.EVENTS).get(DateFilter.upcoming)).
            toBe("api/events.json?from=2017-5-1");
    }));

});
