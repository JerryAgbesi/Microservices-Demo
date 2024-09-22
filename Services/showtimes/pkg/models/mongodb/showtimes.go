package mongodb

import (
	"context"

	"github.com/jerryAgbesi/microservices-demo/showtimes/pkg/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type ShowTimeCollection struct {
	C *mongo.Collection 
}

func (c *ShowTimeCollection) All() ([]models.ShowTimes,error){
	ctx := context.TODO()
	st := []models.ShowTimes{}

	showtimeCursor, err := c.C.Find(ctx,bson.M{})

	if err != nil{
		return nil,err
	}

	err = showtimeCursor.All(ctx,&st)
	if err != nil{
		return nil,err
	}

	return st,err

}