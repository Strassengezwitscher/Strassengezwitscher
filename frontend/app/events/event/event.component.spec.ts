import { Observable } from "rxjs/Rx";
import { TestBed, inject } from "@angular/core/testing";

import { Event, EventComponent, EventService } from "./../";

class MockEventService {
    public getEvent(id: number): Observable<Event> {
        let ev = new Event();
        ev.id = 1;
        ev.name = "Test";
        return new Observable<Event>(observer => {
            observer.next(ev);
            observer.complete();
        });
    }
}

describe("EventComponent", () => {

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                EventComponent,
                {
                    provide: EventService,
                    useClass: MockEventService,
                },
            ],
        });
    });

    it("Should set a new active Event", inject([EventComponent], (evComponent) =>  {
        evComponent.getEvent(1);
        expect(evComponent.event.id).toBe(1);
    }));

    it("Should set a new active Event on ngChange", inject([EventComponent], (evComponent) =>  {
        evComponent.ngOnChanges({"id": 125});
        expect(evComponent.event.name).toBe("Test");
    }));

});
