from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from zones.models import Zone, Distribution
# from zones.api.serializers import ZoneSerializer


@api_view(['POST'])
def edit(request):
    zone_id = request.data.get('id')
    name = request.data.get('name')
    distributions = request.data.get('distributions', False)

    zone = Zone.objects.filter(pk=zone_id).first()
    if not zone:
        return Response('Send zone_id as a body value', status=status.HTTP_400_BAD_REQUEST)

    zone.name = name
    try:
        zone.save()
    except Exception as error:
        return Response('Error 500 internal: {error}'.format(error=error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    if distributions:
        for distribution in distributions:

            try:
                distribution_object = Distribution.objects.filter(pk=distribution['id'], zone=zone_id).first()

                if 'delete' in distribution:

                    if distribution['delete'] == True:
                        distribution_object.delete()

                else:
                    distribution_object.percentage = int(distribution['percentage'])
                    distribution_object.save()
            except Exception as error:
                return Response('Error 500 internal: {error}'.format(error=error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(data=zone.updated_at, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_distribution(request):
    zone_id = request.data.get('zone')
    distribution = request.data.get('distribution', False)

    zone = Zone.objects.filter(pk=zone_id).first()
    if not zone:
        return Response('Zone does not exists', status=status.HTTP_400_BAD_REQUEST)

    if not distribution:
        return Response('Send distribution as a body value', status=status.HTTP_400_BAD_REQUEST)

    try:
        distribution_object = Distribution(
            zone=zone,
            percentage=int(distribution)
        )
        distribution_object.save()
    except Exception as error:
        return Response('Error 500 internal: {error}'.format(error=error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(data={"id": distribution_object.id, "percentage": distribution_object.percentage}, status=status.HTTP_200_OK)
