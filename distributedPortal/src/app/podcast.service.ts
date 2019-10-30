import { Injectable } from '@angular/core';
import { Podcast } from './podcast';
import { PODCASTS } from './mock-podcasts';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PodcastService {

  constructor() { }

  getPodcasts(): Observable<Podcast[]> {
    return of(PODCASTS);
  }
}
