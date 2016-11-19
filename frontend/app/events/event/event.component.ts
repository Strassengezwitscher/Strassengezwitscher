import { Component, EventEmitter, Input, OnChanges, Output } from "@angular/core";

import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";
import { Helper } from "../../helper";

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
    @Output() public onClose = new EventEmitter<boolean>();

    constructor(private eventService: EventService) {}

    public ngOnChanges(changes) {
        if (changes.id !== undefined) {
            this.getEvent(this.id);
        }
    }

    public dateFormat(dateAsString: string) {
        const date: Date = new Date(dateAsString);
        return Helper.regionalDateFormat(date);
    }

    public close() {
        this.onClose.emit(true);
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id).subscribe(
            event => this.event = event,
            error => this.onError.emit(error),
        );
    }
}
