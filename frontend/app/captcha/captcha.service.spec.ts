import { TestBed, inject } from "@angular/core/testing";
import { BaseRequestOptions, Http, Response, ResponseOptions } from "@angular/http";
import { MockBackend } from "@angular/http/testing";

import { CaptchaService } from "./";

describe("CaptchaService", () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                CaptchaService,
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

    it("Should return mocked response", inject([MockBackend, CaptchaService], (mockBackend, service) => {
        let response = [
            {
                "status": "success",
            },
        ];

        mockBackend.connections.subscribe(connection => {
            connection.mockRespond(new Response(new ResponseOptions({body: JSON.stringify(response)})));
        });
        service.validateCaptcha().subscribe(res => {
            expect(res).toContain({
                "status": "success",
            });
        });
    }));

    it("Should return server error message if Internal Server Error occurs",
       inject([MockBackend, CaptchaService], (mockBackend, service) => {
        mockBackend.connections.subscribe(connection => {
            connection.mockError(new Error("Internal Server Error 500"));
        });
        try {
            service.validateCaptcha().subscribe();
        } catch (error) {
            expect(error).toBe("Internal Server Error 500");
        }
    }));

    it("Should return error status code and text if present", inject([CaptchaService], (service) => {
        spyOn(service, "handleError").and.callThrough();
        let err = {statusText: "Resource not found", status: 404};

        expect(service.handleError(err).error).toBe("404 - Resource not found");
    }));

    it("Should return custom error message", inject([CaptchaService], (service) => {
        spyOn(service, "handleError").and.callThrough();
        let err = {_body: '{"errors":["missing-input-secret"] }', status: 400};

        expect(service.handleError(err).error).toBe("Interner Fehler im Captcha: \nmissing-input-secret \n");
    }));
});
