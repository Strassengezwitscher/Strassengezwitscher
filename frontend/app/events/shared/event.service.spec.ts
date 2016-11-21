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

    it("Should return last event without a server request",
        inject([MockBackend, EventService], (mockBackend, service) => {
        spyOn(service.http, "get");
        service.lastEvent = new Event();
        service.lastEvent.id = 1;
        service.getEvent(1).subscribe(res => {
            expect(res.id).toEqual(1);
            expect(service.http.get).toHaveBeenCalledTimes(0);
        });
    }));

    it("Should return fake event response on getEvent",
        inject([MockBackend, EventService], (mockBackend, service, done) => {
        let response = [
            {
                "id": 1,
                "name": "name",
                "location": "Dresden",
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
            });
        });
    }));

    it("Should return fake twitter response on getTweetIds",
        inject([MockBackend, EventService], (mockBackend, service) => {
        let response = ["1", "2"];

        mockBackend.connections.subscribe(connection => {
            connection.mockRespond(new Response(new ResponseOptions({body: JSON.stringify(response)})));
        });
        service.getTweetIds(1).subscribe(res => {
            expect(res).toEqual(["1", "2"]);
        });
    }));

    it("Should return twitter error", inject([MockBackend, EventService], (mockBackend, service) => {
        mockBackend.connections.subscribe(connection => {
            connection.mockError(new Error("Internal Server Error 500"));
        });
        try {
            service.getTweetIds(1).subscribe();
        } catch (error) {
            expect(error).toBe("[]");
        }
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
