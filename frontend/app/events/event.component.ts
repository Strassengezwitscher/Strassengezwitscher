import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";

import { Event, EventService } from "./";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail",
    templateUrl: "event.component.html",
    styleUrls: ["event.component.css"],
    providers: [EventService],
})

export class EventComponent implements OnChanges {
    public activeEvent: Event;
    @Input("id") public id: number;
    @Output() public onError = new EventEmitter<string>();
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
                            error => this.onError.emit(error)
                        );
    }

    private setActiveEvent(event: Event) {
        this.activeEvent = event;
    }
}
