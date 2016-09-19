import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";
import { Router } from "@angular/router";

import { Event, EventService } from "./";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail",
    templateUrl: "event.component.html",
    providers: [EventService],
})

export class EventComponent implements OnChanges {
    private activeEvent: Event;
    @Input("id") private id: number;
    @Output() private onError = new EventEmitter<string>();
    constructor(private eventService: EventService, private router: Router) {
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
    private gotoDetail(): void {
        this.router.navigate(["/event", this.activeEvent.id]);
    }
}
