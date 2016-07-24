import { Injectable }     from "@angular/core";
import { Response }       from "@angular/http";
import { Observable }     from "rxjs/Observable";

@Injectable()
export class ContactService {

    private contactURL = "api/contact/";

    public addContactData (contactData: any, uploads: FileList): Observable<Response> {

        // work around as long as angular2 http does not support multipart-form data
        return Observable.create(observer => {
        let formData: FormData = new FormData(contactData);
        let xhr: XMLHttpRequest = new XMLHttpRequest();

        for (let key in contactData) {
          if (contactData.hasOwnProperty(key)) {
            formData.append(key, contactData[key]);
          }
        }

        // add files seperately
        for (let i = 0; i < uploads.length; ++i) {
          formData.append("files", uploads[i], uploads[i].name);
        }

        xhr.onreadystatechange = () => {
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              observer.next(JSON.parse(xhr.response));
              observer.complete();
            } else {
              observer.error(JSON.parse(xhr.response));
            }
          }
        };

        xhr.open("POST", this.contactURL, true);
        xhr.send(formData);
      });
    }
}
