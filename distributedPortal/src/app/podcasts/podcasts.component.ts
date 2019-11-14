import { Component, OnInit } from '@angular/core';

import { PodcastService } from '../podcast.service';

@Component({
  selector: 'app-podcasts',
  templateUrl: './podcasts.component.html',
  styleUrls: ['./podcasts.component.css']
})
export class PodcastsComponent implements OnInit {

  podcasts: any=[];

  constructor(private podcastService: PodcastService) { }

  getPodcasts() {
    return this.podcastService.getPodcasts()
      .subscribe(
        (content) => {
          this.podcasts = content.data
          this.podcasts.sort((a, b) => (a.EpisodeID > b.EpisodeID) ? 1:-1)
        })
  }

  fileToUpload: File = null;
  handleFileInput(files: FileList) {
    console.log(files)
    this.fileToUpload = files.item(0);
  }

  add(title: string, author: string, id: string): void {
    this.podcastService.addPodcast(title, author, id, this.fileToUpload)
      .subscribe(podcast => {
        
        this.podcasts.push(podcast);
      });
  }

  delete(id:string): void {
    this.podcastService.deletePodcast(id)
      .subscribe(podcast => {
        for(let index =0; index < this.podcasts.length; index++){
          if (this.podcasts[index].EpisodeID == id){
            // console.log(this.podcasts[index].EpisodeID)
            this.podcasts.pop(this.podcasts[index]);
          }
        }
      })
  }

  ngOnInit() {
    this.getPodcasts();
  }

}