import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { MessageService } from './message.service';
import { Podcast } from './podcast';
import { PODCASTS } from './mock-podcasts';

@Injectable({
  providedIn: 'root'
})
export class PodcastService {

  constructor(private messageService: MessageService) { }

  getPodcasts(): Observable<Podcast[]> {
    this.messageService.add('PodcastService: fetched Podcasts')
    return of(PODCASTS);
  }

  getPodcast(EpisodeID: number): Observable<Podcast> {
    this.messageService.add(`PodcastService: fetched podcast EpisodeID=${EpisodeID}`);
    return of(PODCASTS.find(podcast => podcast.EpisodeID === EpisodeID))
  }
}
