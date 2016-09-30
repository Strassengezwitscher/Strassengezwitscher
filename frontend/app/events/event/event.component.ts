import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";

import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail",
    templateUrl: "event.component.html",
    styleUrls: ["event.component.css"],
})

export class EventComponent implements OnChanges {
    public event: Event = null;
    @Input("id") public id: number;
    @Output() public onError = new EventEmitter<string>();

    constructor(private eventService: EventService) {}

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
    }
}
