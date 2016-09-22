import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";

import { Event, EventService } from "./../";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail",
    templateUrl: "event.component.html",
})

export class EventComponent implements OnChanges {
    private event: Event;
    @Input("id") private id: number;
    @Output() private onError = new EventEmitter<string>();
    constructor(private eventService: EventService) {
        this.event = new Event();
    }

    public ngOnChanges(changes) {
        if (changes.id !== undefined) {
            this.getEvent(this.id);
        }
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id)
                        .subscribe(
                            event => this.setActiveEvent(event),
                            error => this.onError.emit(error)
                        );
    }

    private setActiveEvent(ev: Event) {
        this.event = ev;
        this.eventService.setActiveEvent(ev);
    }
}
