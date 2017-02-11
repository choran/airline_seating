from code.lib.seat_assign import Seating

# We can add more here when we know how we want to call it

if __name__ == '__main__':
    print('test')
    seating = Seating()

    seating.parse_args()
    seating.create_connection()
    seating.get_plane_layout()
    seating.populate_seat_availability()
    seating.allocate_bookings()
    seating.populate_statistics()
    seating.destroy_connection()
