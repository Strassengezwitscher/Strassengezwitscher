import { Observable } from "rxjs/Rx";
import { TestBed, inject } from "@angular/core/testing";

import { EventComponent } from "./event.component";
import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";

class MockEventService {
    public getEvent(id: number): Observable<Event> {
        let ev = new Event();
        ev.id = 1;
        ev.name = "Test";
        if (id === 1) {
            return new Observable<Event>(observer => {
                observer.next(ev);
                observer.complete();
            });
        } else {
            return Observable.throw(new Error("error"));
        }
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
        evComponent.id = 1;
        evComponent.ngOnChanges({"id": 125});
        expect(evComponent.event.name).toBe("Test");
    }));

    it("Should throw emit an error", inject([EventComponent], (evComponent) =>  {
        spyOn(evComponent.onError, "emit");
        evComponent.getEvent(10);
        expect(evComponent.onError.emit).toHaveBeenCalledTimes(1);
    }));

    it("Should emit bool to parent class on close", inject([EventComponent], (evComponent) =>  {
        spyOn(evComponent.onClose, "emit");
        evComponent.close();
        expect(evComponent.onClose.emit).toHaveBeenCalledTimes(1);
    }));

    it("Should convert date from yyyy-mm-dd to dd-mm-yyyy", inject([EventComponent], (evComponent) =>  {
        let date = evComponent.dateFormat("2015-12-30");
        expect(date).toBe("30.12.2015");
    }));

});
