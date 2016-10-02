import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";

import { Event, EventService } from "./../";
import { Helper } from "../../helper";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail",
    templateUrl: "event.component.html",
})

export class EventComponent implements OnChanges {
    private event: Event = null;
    @Input("id") private id: number;
    @Output() private onError = new EventEmitter<string>();
    constructor(private eventService: EventService) {}

    public ngOnChanges(changes) {
        if (changes.id !== undefined) {
            this.getEvent(this.id);
        }
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id).subscribe(
            event => this.event = event,
            error => this.onError.emit(error),
        );
    }

    private dateFormat(dateAsString: string) {
        const date: Date = new Date(dateAsString);
        return Helper.regionalDateFormat(date);
    }
}
