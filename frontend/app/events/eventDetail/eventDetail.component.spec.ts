import { Observable } from "rxjs/Rx";
import { TestBed, inject } from "@angular/core/testing";
import { ActivatedRoute } from "@angular/router";

import { Event, EventDetailComponent, EventService } from "./../";

class MockEventService {
    public getEvent(id: number): Observable<Event> {
        if (id > 0) {
            let ev = new Event();
            ev.id = 1;
            ev.name = "Test";
            return new Observable<Event>(observer => {
                observer.next(ev);
                observer.complete();
            });
        } else {
            return Observable.throw("Error wrong ID");
        }
    }

    public getTweetIds(event: Event): Observable<string[]> {
        return Observable.of(["1"]);
    }
}

describe("EventDetailComponent", () => {

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                EventDetailComponent,
                {
                    provide: ActivatedRoute,
                },
                {
                    provide: EventService,
                    useClass: MockEventService,
                },
            ],
        });
    });

    it("Should set a new active Event", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.getEvent(1);
        expect(evDComponent.event.id).toBe(1);
    }));

    it("Should set the error message on error from service", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.getEvent(-100);
        expect(evDComponent.errorMessage).toBe("Error wrong ID");
    }));

    it("Should set the error Message", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.setErrorMessage("ErrorMessage");
        expect(evDComponent.errorMessage).toBe("ErrorMessage");
    }));

    it("Should clear the error Message again", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.setErrorMessage("ErrorMessage");
        expect(evDComponent.errorMessage).toBe("ErrorMessage");
        evDComponent.clearError();
        expect(evDComponent.errorMessage).toBe("");
    }));

});
