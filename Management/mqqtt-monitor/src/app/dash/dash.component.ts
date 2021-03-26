import {Component, ElementRef, ViewChild} from '@angular/core';
import {map} from 'rxjs/operators';
import {Breakpoints, BreakpointObserver} from '@angular/cdk/layout';
import {Subscription} from 'rxjs';
import {IMqttMessage, MqttService} from 'ngx-mqtt';
import {ChartDataSets, ChartType, RadialChartOptions} from 'chart.js';
import {BaseChartDirective, Label} from 'ng2-charts';
import {randomInt} from 'node:crypto';

@Component({
  selector: 'app-dash',
  templateUrl: './dash.component.html',
  styleUrls: ['./dash.component.scss']
})
export class DashComponent {

  // tslint:disable-next-line:variable-name
  constructor(private breakpointObserver: BreakpointObserver, private _mqttService: MqttService) {
  }

  /** Based on the screen size, switch from standard to one column per row */
  title = 'Dashboard';
  private subscription: Subscription;
  topicHR = '/channel/HR-sensor';
  topicTEMP = '/channel/TEMP-sensor';
  topicBLANKET = '/channel/BLANKET-sensor';
  topicPredictionBLANKET = '/channel/BLANKET-prediction';
  msgHR: any;
  msgBLANKED: any;
  msTEMP: any;
  msgPredictionBLANKET: any;
  isConnected = false;

  @ViewChild(BaseChartDirective)
  public chart: BaseChartDirective;

  // Radar
  public radarChartOptions: RadialChartOptions = {
    responsive: true,
  };
  public radarChartLabels: Label[] = ['HR', 'BLANKET', 'TEMPERATURE', 'PREDICTION'];

  public radarChartData: ChartDataSets[] = [
    {data: [65, 59, 90, 81], label: 'Situation'}
  ];
  public radarChartType: ChartType = 'radar';


  ngOnInit(): void {
    this.subscribeNewTopicPredictionBLANKET();
    this.subscribeNewTopicHR();
    this.subscribeNewTopicBLANKET();
    this.subscribeNewTopicTEMP();

  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  subscribeNewTopicHR(): void {
    this.subscription = this._mqttService
      .observe(this.topicHR)
      .subscribe((message: IMqttMessage) => {
        // tslint:disable-next-line:no-unused-expression
        // @ts-ignore
        this.radarChartData[0].data[0] = message.payload.toString();
        // tslint:disable-next-line:no-unused-expression
        this.chart.chart.update();
      });
  }

  subscribeNewTopicBLANKET(): void {
    this.subscription = this._mqttService
      .observe(this.topicBLANKET)
      .subscribe((message: IMqttMessage) => {
        // tslint:disable-next-line:no-unused-expression
        // @ts-ignore
        this.radarChartData[0].data[1] = message.payload.toString();
        // tslint:disable-next-line:no-unused-expression
        this.chart.chart.update();
      });
  }

  subscribeNewTopicTEMP(): void {
    this.subscription = this._mqttService
      .observe(this.topicTEMP)
      .subscribe((message: IMqttMessage) => {
        // tslint:disable-next-line:no-unused-expression
        // @ts-ignore
        this.radarChartData[0].data[2] = message.payload.toString();
        // tslint:disable-next-line:no-unused-expression
        this.chart.chart.update();
      });
  }

  subscribeNewTopicPredictionBLANKET(): void {
    this.subscription = this._mqttService
      .observe(this.topicPredictionBLANKET)
      .subscribe((message: IMqttMessage) => {
        // tslint:disable-next-line:no-unused-expression
        // @ts-ignore
        this.radarChartData[0].data[3] = message.payload.toString();
        console.log(message.payload.toString());
        // tslint:disable-next-line:no-unused-expression
        this.chart.chart.update();
      });
  }

  /*sendHRmsg(): void {
    // use unsafe publish for non-ssl websockets
    this._mqttService.unsafePublish(this.topicHR, this.msgHR, {
      qos: 1,
      retain: true
    });
    this.msgHR = '';
  }*/

}
