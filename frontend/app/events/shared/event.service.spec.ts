import { TestBed, inject } from "@angular/core/testing";
import { BaseRequestOptions, Http, Response, ResponseOptions } from "@angular/http";
import { MockBackend } from "@angular/http/testing";

import { EventService } from "./event.service";
import { Event } from "./event.model";

describe("EventService", () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                EventService,
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

    it("Should return mocked response from last Event", inject([MockBackend, EventService], (mockBackend, service) => {
        service.lastEvent = new Event();
        service.lastEvent.id = 1;
        service.getEvent(1).subscribe(res => {
            expect(res.id).toEqual(1);
        });
    }));

    it("Should return mocked response", inject([MockBackend, EventService], (mockBackend, service) => {
        let response = [
            {
                "id": 1,
                "name": "name",
                "location": "Dresden",
                "events": [1, 2],
                "notes": "Note",
                "facebookId": "10",
            },
        ];

        mockBackend.connections.subscribe(connection => {
            connection.mockRespond(new Response(new ResponseOptions({body: JSON.stringify(response)})));
        });
        service.getEvent(1).subscribe(res => {
            expect(res).toContain({
                "id": 1,
                "name": "name",
                "location": "Dresden",
                "events": [1, 2],
                "notes": "Note",
                "facebookId": "10",
            });
        });
    }));

    it("Should return server error message if Internal Server Error occurs",
       inject([MockBackend, EventService], (mockBackend, service) => {
        mockBackend.connections.subscribe(connection => {
            connection.mockError(new Error("Internal Server Error 500"));
        });
        try {
            service.getEvent(1).subscribe();
        } catch (error) {
            expect(error).toBe("Internal Server Error 500");
        }
    }));

    it("Should return error status code and text if present",
        inject([MockBackend, EventService], (mockBackend, service) => {
        spyOn(service, "handleError").and.callThrough();
        let err = {statusText: "Resource not found", status: 404};

        expect(service.handleError(err).error).toBe("404 - Resource not found");
    }));
});
