import { Observable } from "rxjs/Rx";
import { TestBed, inject } from "@angular/core/testing";
import { Router } from "@angular/router";

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

class FakeRouter {
    public navigateByUrl(url: string) { return url;  }
}

describe("EventComponent", () => {

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                EventComponent,
                {
                    provide: Router,
                    useClass: FakeRouter,
                },
                {
                    provide: EventService,
                    useClass: MockEventService,
                },
            ],
        });
    });

    it("Should set the active Event", inject([EventComponent], (evComponent)  => {
        let ev = new Event();
        evComponent.setActiveEvent(ev);
        expect(evComponent.activeEvent).toBe(ev);
    }));

    it("Should set a new active Event", inject([EventComponent], (evComponent) =>  {
        evComponent.getEventDetails(1);
        expect(evComponent.activeEvent.id).toBe(1);
    }));

    it("Should set a new active Event on ngChange", inject([EventComponent], (evComponent) =>  {
        evComponent.ngOnChanges({"id": 125});
        expect(evComponent.activeEvent.name).toBe("Test");
    }));

});
