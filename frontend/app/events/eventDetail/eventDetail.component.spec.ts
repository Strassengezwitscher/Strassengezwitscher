import { Observable } from "rxjs/Rx";
import { TestBed, inject } from "@angular/core/testing";
import { ActivatedRoute } from "@angular/router";

import { EventDetailComponent } from "./eventDetail.component";
import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";

class MockEventService {
    public getEvent(id: number): Observable<Event> {
        if (id > 0) {
            let ev = new Event();
            ev.id = id;
            ev.name = "Test";
            if (id === 2) {
                ev.coverage = true;
            }
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

class MockRoute {
    public params = [{"id" : 1}];
}

describe("EventDetailComponent", () => {

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                EventDetailComponent,
                {
                    provide: ActivatedRoute,
                    useClass: MockRoute,
                },
                {
                    provide: EventService,
                    useClass: MockEventService,
                },
            ],
        });
    });

    it("Should set a new active & not covered Event", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.getEvent(1);
        expect(evDComponent.event.id).toBe(1);
        expect(evDComponent.tweetIds).toEqual(null);
    }));

    it("Should set a new active & covered Event", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.getEvent(2);
        expect(evDComponent.event.id).toBe(2);
        expect(evDComponent.tweetIds).toEqual(["1"]);
    }));

    it("Should set the error message on error from service", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.getEvent(-100);
        expect(evDComponent.errorMessage).toBe("Error wrong ID");
    }));

    it("Should set the error Message", inject([EventDetailComponent], (evDComponent) =>  {
        evDComponent.setErrorMessage("ErrorMessage");
        expect(evDComponent.errorMessage).toBe("ErrorMessage");
    }));

    it("Should call getTweetIds on refreshTweetIds", inject([EventDetailComponent], (evDComponent) =>  {
        spyOn(evDComponent.eventService, "getTweetIds").and.callThrough();
        expect(evDComponent.tweetIds).toEqual(null);
        evDComponent.refreshTweetIds();
        expect(evDComponent.tweetIds).toEqual(["1"]);
        expect(evDComponent.eventService.getTweetIds).toHaveBeenCalledTimes(1);
    }));

    it("Should call getEvent on ngOnInit", inject([EventDetailComponent], (evDComponent) =>  {
        spyOn(evDComponent.eventService, "getEvent").and.callThrough();
        evDComponent.ngOnInit();
        expect(evDComponent.eventService.getEvent).toHaveBeenCalledTimes(1);
    }));

});
