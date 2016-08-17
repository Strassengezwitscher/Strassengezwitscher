import { Component, Input, OnChanges } from "@angular/core";

import { Event } from "./event";
import { EventService } from "./event.service";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail",
    templateUrl: "event.component.html",
    providers: [EventService],
})

export class EventComponent implements OnChanges {
    private activeEvent: Event;
    @Input("id") private id: number;
    constructor(private eventService: EventService) {
        this.activeEvent = new Event();
    }

    public ngOnChanges(changes) {
        if (changes.id !== undefined) {
            this.getEventDetails(this.id);
        }
    }

    private getEventDetails(id: number) {
        this.eventService.getEvent(id)
                        .subscribe(
                            event => this.setActiveEvent(event),
                            error => console.log(error)
                        );
    }

    private setActiveEvent(event: Event) {
        this.activeEvent = event;
    }
}
